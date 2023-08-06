from .enums import EventOperationID, AgentAIType


def transcode(op: EventOperationID, data: dict):
    transcode_data = data

    if op == EventOperationID.EVT_EXT_ASL_RESULT:
        if data["label_type"] != 0:  # Classification
            transcode_data = {
                "label_type": data["label_type"],
                "confidence": data["confidence"],
                "label": data["result"][0]
            }
        else:
            transcode_data = {
                "confidence": data["confidence"],
                "regression": data["result"]
            }

    elif op == EventOperationID.EVT_EXT_VM_RESULT:
        if data["ai_type"] == AgentAIType.APP_AI_TYPE_CLASSIFICATION.value:
            results = data["result"]
            res_nb = int(len(results) / 2)
            confidences = {}
            for k in range(res_nb):
                confidences[results[2 * k + 1]] = results[2 * k]

            transcode_data = {
                "ai_type": data["ai_type"],
                "label_type": data["label_type"],
                "step": data["step"],
                "confidences": confidences
            }

        else:
            transcode_data = {
                "ai_type": data["ai_type"],
                "label_type": data["label_type"],
                "step": data["step"],
                "regression": data["result"]
            }

    return transcode_data
