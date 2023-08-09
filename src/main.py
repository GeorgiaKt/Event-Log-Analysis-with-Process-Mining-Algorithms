import pm4py
import os
from pm4py.objects.log.importer.xes import importer as xes_import
from pm4py import convert_to_dataframe
from pm4py.objects.conversion.log import converter as stream_converter #for eventstream
from pm4py.statistics.end_activities.log.get import get_end_activities
from pm4py.statistics.start_activities.log.get import get_start_activities
from pm4py.algo.filtering.log.end_activities import end_activities_filter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.evaluation import algorithm as evaluation
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay


def main():
    # Reading and printing event log - 1,2
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'event_log_file', 'edited_hh102_labour.xes')
    log = xes_import.apply(log_file) # read event log 'edited_hh102_labour.xes'
    dataframe = convert_to_dataframe(log) # convert event log to dataframe
    print(dataframe) # print dataframe - structure of the traces and events is visible
    # or
    # print(log)
    print("\n\n")



    # Printing number of traces, events - 3,4
    print("Number of traces: ", len(log))
    event_stream = stream_converter.apply(log, variant=stream_converter.Variants.TO_EVENT_STREAM) # convert log to event stream
    print("Number of events: ", len(event_stream))
    print("\n\n")



    # Printing the different-unique events from the event log - 5
    unique_events_df = dataframe.drop_duplicates(subset='concept:name') # keep only the unique events
    unique_events = unique_events_df['concept:name'].tolist() # get the unique events as a list
    print("Events used: ",unique_events)
    print("\n\n")



    # Printing first & last events and their frequencies - 6
    #  group based on the caseId (name of the event) and ...
    first_activities = dataframe.groupby('case:concept:name')['concept:name'].first().value_counts() # retrieve first event for each case
    last_activities = dataframe.groupby('case:concept:name')['concept:name'].last().value_counts() # retrieve last event for each case
    # value_counts() calculates the frequency of first and last events
    # printing
    print("First Activities:")
    for activity, frequency in first_activities.items():
        print(f"Activity: {activity}, Frequency: {frequency}")
    print("Last Activities:")
    for activity, frequency in last_activities.items():
        print(f"Activity: {activity}, Frequency: {frequency}")
    # or
    # end_activities = get_end_activities(log)
    # start_activities = get_start_activities(log)
    # print(start_activities)
    # print(end_activities)
    print("\n\n")



    # Printing case id, activity name, transition (start/complete), timestamp in a table - 7
    table = dataframe[['case:concept:name', 'concept:name', 'lifecycle:transition', 'time:timestamp']]
    table.columns = ['CaseID', 'ActivityName', 'Transition', 'Timestamp']
    print(table)
    print("\n\n")



    # Filtering based on what the last activities are and printing - 8
    filtered_log = end_activities_filter.apply(log, ['End']) # filter-keep traces that end with the "end"
    print('Number of traces of filtered log: ',len(filtered_log))
    print(filtered_log)
    # getting 0 results for 'end', 15 results for 'End'
    print("\n\n")



    # Discovering process models - 9    &   Evaluating each of the process models - 10      &   Conformance checking using Replay fitness - 11
    # Alpha Miner
    # initial log
    net, initial_marking, final_marking = alpha_miner.apply(log) # apply alpha miner to log
    gviz = pn_visualizer.apply(net, initial_marking, final_marking) # create graph
    pn_visualizer.view(gviz) # visualize graph

    # Evaluating for Alpha Miner - log (10)
    evaluation_result = evaluation.apply(log, net, initial_marking, final_marking)
    print('Evaluation result (Alpha Miner - log):')
    print (evaluation_result)

    # Conformance checking using Replay fitness - Alpha Miner, log (11)
    count = 0 # counter for the number of non-fit traces found
    replayed_traces = token_replay.apply(log, net, initial_marking, final_marking)
    for trace in replayed_traces:
        for key, value in trace.items():
            if key == 'trace_is_fit' and value == False: # if trace's key has value False then increase counter
                count+=1
    print("Number of replayed traces: ", len(replayed_traces))
    print("Number of non-fit traces (Alpha Miner - log): ",count)
    # print(replayed_traces)

    # filtered log (traces that end with 'End' - since there are 0 results for 'end') 
    net, initial_marking, final_marking = alpha_miner.apply(filtered_log) # apply alpha miner to filtered log
    gviz = pn_visualizer.apply(net, initial_marking, final_marking) # create graph
    pn_visualizer.view(gviz) # visualize graph

    # Evaluating for Alpha Miner - filtered log (10)
    evaluation_result = evaluation.apply(filtered_log, net, initial_marking, final_marking)
    print('Evaluation result (Alpha Miner - filtered log):')
    print (evaluation_result)

    # Conformance checking using Replay fitness - Alpha Miner, filtered log (11)
    count = 0 # counter for the number of non-fit traces found
    replayed_traces = token_replay.apply(filtered_log, net, initial_marking, final_marking)
    for trace in replayed_traces:
        for key, value in trace.items():
            if key == 'trace_is_fit' and value == False: # if trace's key has value False then increase counter
                count+=1
    print("Number of replayed traces: ", len(replayed_traces))
    print("Number of non-fit traces (Alpha Miner - filtered log): ",count)
    # print(replayed_traces)

    print("\n")


    # Heuristics Miner
    # initial log
    net, initial_marking, final_marking = heuristics_miner.apply(log) # apply heuristics miner to log
    gviz = pn_visualizer.apply(net, initial_marking, final_marking) # create graph
    pn_visualizer.view(gviz) # visualize graph

    # Evaluating for Heuristics Miner - log (10)
    evaluation_result = evaluation.apply(log, net, initial_marking, final_marking)
    print('Evaluation result (Heuristics Miner - log):')
    print (evaluation_result)

    # Conformance checking using Replay fitness - Heuristics Miner, log (11)
    count = 0 # counter for the number of non-fit traces found
    replayed_traces = token_replay.apply(log, net, initial_marking, final_marking)
    for trace in replayed_traces:
        for key, value in trace.items():
            if key == 'trace_is_fit' and value == False: # if trace's key has value False then increase counter
                count+=1
    print("Number of replayed traces: ", len(replayed_traces))
    print("Number of non-fit traces (Heuristics Miner - log): ",count)
    # print(replayed_traces)

    # filtered log (traces that end with 'End' - since there are 0 results for 'end') 
    net, initial_marking, final_marking = heuristics_miner.apply(filtered_log) # apply heuristics miner to filtered log
    gviz = pn_visualizer.apply(net, initial_marking, final_marking) # create graph
    pn_visualizer.view(gviz) # visualize graph

    # Evaluating for Heuristics Miner - filtered log (10)
    evaluation_result = evaluation.apply(filtered_log, net, initial_marking, final_marking)
    print('Evaluation result (Heuristics Miner - filtered log):')
    print (evaluation_result)

    # Conformance checking using Replay fitness - Heuristics Miner, filtered log (11)
    count = 0 # counter for the number of non-fit traces found
    replayed_traces = token_replay.apply(filtered_log, net, initial_marking, final_marking)
    for trace in replayed_traces:
        for key, value in trace.items():
            if key == 'trace_is_fit' and value == False: # if trace's key has value False then increase counter
                count+=1
    print("Number of replayed traces: ", len(replayed_traces))
    print("Number of non-fit traces (Heuristics Miner - filtered log): ",count)
    # print(replayed_traces)

    print("\n")


    # Inductive Miner
    # initial log
    tree = inductive_miner.apply(log) # apply inductive miner to log
    net, initial_marking, final_marking = pm4py.convert_to_petri_net(tree) # convert process tree to petrinet
    gviz= pn_visualizer.apply(net, initial_marking, final_marking) # create graph
    pn_visualizer.view(gviz) # visualize graph

    # Evaluating for Inductive Miner - log (10)
    evaluation_result = evaluation.apply(log, net, initial_marking, final_marking)
    print('Evaluation result (Inductive Miner - log):')
    print (evaluation_result)

    # Conformance checking using Replay fitness - Inductive Miner, log (11)
    count = 0 # counter for the number of non-fit traces found
    replayed_traces = token_replay.apply(log, net, initial_marking, final_marking)
    for trace in replayed_traces:
        for key, value in trace.items(): # if trace's key has value False then increase counter
            if key == 'trace_is_fit' and value == False:
                count+=1
    print("Number of replayed traces: ", len(replayed_traces))
    print("Number of non-fit traces (Inductive Miner - log): ",count)
    # print(replayed_traces)

    # filtered log (traces that end with 'End' - since there are 0 results for 'end')
    tree = inductive_miner.apply(filtered_log) # apply inductive miner to filtered log
    net, initial_marking, final_marking = pm4py.convert_to_petri_net(tree) # convert process tree to petrinet
    gviz= pn_visualizer.apply(net, initial_marking, final_marking) # create graph
    pn_visualizer.view(gviz) # visualize graph

    # Evaluating for Inductive Miner - filtered log (10)
    evaluation_result = evaluation.apply(filtered_log, net, initial_marking, final_marking)
    print('Evaluation result (Inductive Miner - filtered log):')
    print (evaluation_result)

    # Conformance checking using Replay fitness - Inductive Miner, filtered log (11)
    count = 0 # counter for the number of non-fit traces found
    replayed_traces = token_replay.apply(filtered_log, net, initial_marking, final_marking)
    for trace in replayed_traces:
        for key, value in trace.items(): # if trace's key has value False then increase counter
            if key == 'trace_is_fit' and value == False:
                count+=1
    print("Number of replayed traces: ", len(replayed_traces))
    print("Number of non-fit traces (Inductive Miner - filtered log): ",count)
    # print(replayed_traces)


if __name__ == "__main__":
    main()