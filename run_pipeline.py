from app.services.pipeline import process_meeting

from app.utils.logger import logger

import json


logger.info("Starting AI MoM application...")

file_path = ("D:\\Sisindokom\\AI-MoM-Notaker\\input\\meeting_detailed.txt")

final_result = process_meeting(file_path)

with open("outputs/meeting_summary.json","w",encoding="utf-8") as f:

    json.dump(final_result, f, indent=4, ensure_ascii=False)

logger.info("Output JSON saved successfully.")

print("\n===== FINAL SUMMARY =====\n")

print(final_result["summary"])

print("\n===== KEY DISCUSSIONS =====\n")

for discussion in final_result["key_discussions"]:

    print(f"- {discussion}")

print("\n===== DECISIONS =====\n")

for decision in final_result["decisions"]:

    print(f"- {decision}")

print("\n===== ACTION ITEMS =====\n")

for action in final_result["action_items"]:

    print(f"- {action}")

logger.info("Process completed successfully.")