import datetime
import json

class Tools:
    """Tool."""

    def convert_data(self, input_query, return_id=False, json_render=True):
        """Returns json."""
        # make it always a list
        if isinstance(input_query, dict):
            input_query = [input_query]
        temp_data = []
        for data in input_query:
            # remove _id from return
            if not return_id and '_id' in data.keys():
                del data['_id']
            elif '_id' in data.keys():
                # ObjectId to string hehe
                data["id"] = str(data['_id']).replace("ObjectId('", '').replace("'", '')
                del data['_id']
            for k in data.keys():
                # convert datetime to string
                if isinstance(data[k], datetime.datetime):
                    data[k] = data[k].strftime("%d/%m/%Y, %H:%M:%S")
            temp_data.append(data)
        if json_render:
            return json.dumps(temp_data)
        return temp_data
