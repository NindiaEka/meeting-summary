def aggregate_results(all_results):

    final_summary = []
    final_discussions = []
    final_decisions = []
    final_action_items = []

    for result in all_results:

        # combine summary
        final_summary.append(
            result.get("summary", "")
        )

        # combine key discussions
        final_discussions.extend(
            result.get("key_discussions", [])
        )

        # combine decisions
        final_decisions.extend(
            result.get("decisions", [])
        )

        # combine action items
        final_action_items.extend(
            result.get("action_items", [])
        )

    return {
        "summary": "\n".join(final_summary),
        "key_discussions": final_discussions,
        "decisions": final_decisions,
        "action_items": final_action_items
    }

def combine_chunk_summaries(all_results):
    summaries = []

    for result in all_results:
        summaries.append(
            result.get("summary", "")
        )

    return "\n".join(summaries)