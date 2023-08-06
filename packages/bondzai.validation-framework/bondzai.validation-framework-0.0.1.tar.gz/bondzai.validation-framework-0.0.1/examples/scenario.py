import threading
import time

import numpy as np
from bondzai.gateway_sdk import Gateway, AgentAIMode, Agent, AgentTriggerType
from bondzai.gateway_sdk.enums import EventOperationID, DBMTable
from bondzai.validation_framework.log_handler import array_to_str, logger, lines_to_str, Color
from bondzai.validation_framework.result_handler import EXPECTED, PREDICTED
from bondzai.validation_framework.dataset_handler import Dataset, Data
from bondzai.validation_framework.event_catcher import EventCatcher
from bondzai.validation_framework.result_handler import ResultGatherer
from pathlib import Path
import argparse

# To be run with OCR agent
DEFAULT_CHUNK_RATE = 100
DEFAULT_CHUNK_SIZE = 1024


def training_is_done(agent: Agent, status):
    logger.info(f"EVT TRAIN : {status}")


def log_print(agent: Agent, log_message):
    logger.info(log_message)


def print_event(agent: Agent, event_id: EventOperationID, data: dict):
    logger.info(f"EVT {event_id.value} : {data}")


def print_event_final(agent: Agent, data: dict):
    logger.info(f"EVT FINALE {data}")


def print_event_infer(agent: Agent, data: dict):
    logger.info(f"EVT INFER {data}")


def set_callbacks(agent: Agent):
    # Set callbacks
    agent.on_log(log_print)
    agent.on_event(print_event)
    agent.on_training_done(training_is_done)
    agent.on_inference_done(print_event_infer)
    agent.on_final_process_done(print_event_final)


def force_train(agent: Agent):
    """
    Force agent to train
    """
    event_catcher = EventCatcher()
    agent.set_ai_mode(AgentAIMode.APP_AI_MODE_ENROLLEMENT, [0, 0])
    time.sleep(0.5)
    agent.set_ai_mode(AgentAIMode.APP_AI_MODE_INFERENCE)
    event_catcher.wait_training(agent)


def infer_one(agent: Agent, data: Data, start_trigger: AgentTriggerType = AgentTriggerType.TRIGGER_ON,
              end_trigger: AgentTriggerType = AgentTriggerType.TRIGGER_ON,
              chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_rate: int = DEFAULT_CHUNK_RATE):
    """
    Perform one inference
    Args:
        agent: Agent object
        data: Data object
        start_trigger: If needed, define function used for start trigger
        end_trigger: If needed, define function used for end trigger
        chunk_size: Size of one chunk
        chunk_rate: chunk rate (in chunk/s)
    """
    if start_trigger is not None:
        agent.trigger(start_trigger)
    data.send_input_to_agent(agent, chunk_size, chunk_rate)
    if end_trigger is not None:
        agent.trigger(end_trigger)


def infer_all(agent: Agent, dataset: Dataset, start_trigger: AgentTriggerType = AgentTriggerType.TRIGGER_ON,
              end_trigger: AgentTriggerType = AgentTriggerType.TRIGGER_OFF, chunk_size: int = DEFAULT_CHUNK_SIZE,
              chunk_rate: int = DEFAULT_CHUNK_RATE, save_path: Path = None) -> dict:
    """

    Args:
        agent: Agent object
        dataset: dataset object
        start_trigger: If needed, define function used for start trigger
        end_trigger: If needed, define function used for end trigger
        chunk_size: Size of one chunk
        chunk_rate: chunk rate (in chunk/s)
        save_path: path of JSON file to save data
    Returns:
        results: results as dict
    """
    res = ResultGatherer(agent)
    event_catcher = EventCatcher()
    for data in dataset.iter_source():
        infer_one(agent, data, start_trigger, end_trigger, chunk_size, chunk_rate)
        wait_time, infer_result = event_catcher.wait_final_process(agent)
        logger.info(f"Wait for {np.round(wait_time, 2)}s")
        if infer_result is None:
            logger.warning("Missed inference")
        else:
            infer_data = dataset.update_data_from_event(data, infer_result)
            data.add_to_expected_result(res)
            infer_data.add_to_predicted_result(res)
    results = res.get_results(save_path)
    return results


def infer_all_no_wait(agent: Agent, res: ResultGatherer, dataset: Dataset,
                      start_trigger: AgentTriggerType = AgentTriggerType.TRIGGER_ON,
                      end_trigger: AgentTriggerType = AgentTriggerType.TRIGGER_OFF,
                      chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_rate: int = DEFAULT_CHUNK_RATE):
    for data in dataset.iter_source():
        infer_one(agent, data, start_trigger, end_trigger, chunk_size, chunk_rate)
        data.add_to_expected_result(res)
    time.sleep(0.5)


def infer_all_async(agent: Agent, dataset: Dataset, start_trigger: AgentTriggerType = AgentTriggerType.TRIGGER_ON,
                    end_trigger: AgentTriggerType = AgentTriggerType.TRIGGER_OFF, chunk_size: int = DEFAULT_CHUNK_SIZE,
                    chunk_rate: int = DEFAULT_CHUNK_RATE, save_path: Path = None):
    res = ResultGatherer(agent)
    event_catcher = EventCatcher()
    infer_thread = threading.Thread(target=lambda: infer_all_no_wait(agent, res, dataset, start_trigger,
                                                                     end_trigger, chunk_size, chunk_rate), daemon=True)
    infer_thread.start()
    empty_counter = 0
    stop = False
    data_list = []
    while not stop:
        if not infer_thread.is_alive():
            stop = True
        time.sleep(0.5)
        _data_list = event_catcher.get_final_process_data(agent)
        if len(_data_list) == 0:
            empty_counter += 1
        data_list += _data_list
    res_dict = res.get_results_as_list()
    nb_infer_sent = len(list(res_dict.values())[0])
    nb_infer_received = len(data_list)

    if nb_infer_received < nb_infer_sent:
        missed_number = nb_infer_sent - nb_infer_received
        loss_percent = np.round(100 * missed_number / nb_infer_sent, 2)
        logger.warning(f"{missed_number} inferences missed among {nb_infer_sent} inferences ({loss_percent}% loss)")
    else:
        label_type_number = len(dataset.outputs)
        for index, data in enumerate(dataset.iter_source()):
            infer_list = data_list[index * label_type_number: (index + 1) * label_type_number]
            infer_data = dataset.update_data_from_event(data, *infer_list)
            infer_data.add_to_predicted_result(res)
    results = res.get_results(save_path)
    return results


def standard(dataset_path: Path, agent: Agent, sync: bool = True, chunk_size: int = DEFAULT_CHUNK_SIZE,
             chunk_rate: int = DEFAULT_CHUNK_RATE, save_path: Path = None):
    set_callbacks(agent)

    logger.info("---- Switch to infer ----")
    force_train(agent)

    logger.info("---- Get KPI ----")
    kpi = agent.get_kpi()
    logger.info(kpi)

    logger.info("---- Start inferences ----")
    dataset = Dataset(dataset_path, agent)

    if sync:
        results = infer_all(agent=agent,
                            dataset=dataset,
                            save_path=save_path,
                            start_trigger=AgentTriggerType.TRIGGER_ON,
                            end_trigger=AgentTriggerType.TRIGGER_OFF,
                            chunk_size=chunk_size,
                            chunk_rate=chunk_rate)
    else:
        results = infer_all_async(agent=agent,
                                  dataset=dataset,
                                  save_path=save_path,
                                  start_trigger=AgentTriggerType.TRIGGER_ON,
                                  end_trigger=AgentTriggerType.TRIGGER_OFF,
                                  chunk_size=chunk_size, chunk_rate=chunk_rate)

    for key, value in results.items():
        accuracy = np.round(value['accuracy'] * 100, 2) if value["accuracy"] is not None else None
        logger.info(f"\n{key}\n{array_to_str(value['confusion_matrix'])}"
                    f"\n\nAccuracy : {accuracy}%")

    kill(agent)


def incremental_learning(dataset_path: Path, agent: Agent, chunk_size: int = DEFAULT_CHUNK_SIZE,
                         chunk_rate: int = DEFAULT_CHUNK_RATE):
    CORRECTION_RATIO_THRESHOLD = 0.20
    ACCURACY_THRESHOLD = 0.9

    set_callbacks(agent)

    logger.info("---- Switch to infer ----")
    force_train(agent)

    logger.info("---- Get KPI ----")
    kpi = agent.get_kpi()
    logger.info(kpi)

    logger.info("---- Start inferences ----")
    dataset = Dataset(dataset_path, agent)
    label_type = dataset.get_output_type_list()[0]

    event_catcher = EventCatcher()
    accuracy_vect = [0]
    correction_percent = 0
    exclusion_list = []
    to_correct = True
    counter = 0
    while to_correct and correction_percent < CORRECTION_RATIO_THRESHOLD and accuracy_vect[-1] < ACCURACY_THRESHOLD:
        counter += 1
        to_correct = False
        # Test on all dataset
        results = infer_all(agent, dataset, start_trigger=AgentTriggerType.TRIGGER_ON,
                            end_trigger=AgentTriggerType.TRIGGER_OFF, chunk_size=chunk_size, chunk_rate=chunk_rate)
        result_list = results[label_type]["raw_results"]
        accuracy_vect.append(results[label_type]["accuracy"])
        infer_nb = len(result_list)
        if len(exclusion_list) == infer_nb:
            break
        for key, element in result_list.items():
            if key not in exclusion_list:
                # If not needed to be corrected add to exclusion list
                exclusion_list.append(key)
                # If mismatch between prediction and expectation, perform correction
                if element[PREDICTED] != element[EXPECTED]:
                    correction_percent += 1 / infer_nb
                    to_correct = True
                    data = dataset.get_data_by_file_name(key)
                    infer_one(agent, data, start_trigger=AgentTriggerType.TRIGGER_ON,
                              end_trigger=AgentTriggerType.TRIGGER_OFF, chunk_rate=DEFAULT_CHUNK_RATE)
                    event_catcher.wait_final_process(agent)
                    data.send_correction_to_agent(agent, position=0)
                    force_train(agent)
                    break

    logger.info(lines_to_str(accuracy_vect[1:], colors=[Color.RED],
                             title="Incremental learning",
                             x_title="Number of corrections",
                             y_title="Accuracy"))

    time.sleep(0.5)

    agent.kill()


def kill(agent: Agent):
    agent.kill()


def export_dataset(agent: Agent):
    data = agent.export_table_data(DBMTable.DBM_DAT)
    logger.info(data)

    agent.kill()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Run standard scenario")
    parser.add_argument("dataset", type=Path, help="Path of the dataset tar.gz file")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="Path of the JSON file where inference results are saved")
    parser.add_argument("-s", "--size", type=int, default=DEFAULT_CHUNK_SIZE,
                        help=f"Chunk size (by default {DEFAULT_CHUNK_SIZE})")
    parser.add_argument("-r", "--rate", type=int, default=DEFAULT_CHUNK_RATE,
                        help=f"Chunk rate (by default {DEFAULT_CHUNK_RATE})")
    parser.add_argument("-a", "--asynchro", action="store_true",
                        help="If given, run scenario in async mode")
    parser.add_argument("-gh", "--host", type=str, default="127.0.0.1", help="Gateway host")
    parser.add_argument("-gp", "--port", type=int, default=8765, help="Gateway port")
    parser.add_argument("-i", "--incremental", action="store_true",
                        help="If given, run incremental learning scenario instead")
    args = parser.parse_args()

    gateway = Gateway(args.host, args.port)
    gateway.connect()
    logger.info("WAITING")
    agents = gateway.wait_for_agent()
    if agents:
        logger.info("STARTING")
        current_agent = agents[0]
        current_agent.subscribe()
        if args.incremental:
            incremental_learning(dataset_path=args.dataset,
                                 agent=current_agent,
                                 chunk_size=args.size,
                                 chunk_rate=args.rate)
        else:
            standard(dataset_path=args.dataset,
                     agent=current_agent,
                     sync=not args.asynchro,
                     save_path=args.output,
                     chunk_size=args.size,
                     chunk_rate=args.rate)

    gateway.close()
