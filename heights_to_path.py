import json


def getPath(data_file):
    path = []
    with open(data_file, "r") as f:
        data = json.load(f)
        prev_chunk = data[0]
        for i, chunk in enumerate(data[1:]):
            distance = chunk["distance"] - prev_chunk["distance"]
            path.append({'distance': distance,
                        'gradient': round((chunk["height"] - prev_chunk["height"]) / distance, 4),
                         'max_speed': 30})

            prev_chunk = chunk

    return path
