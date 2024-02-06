


def get_new_stage_id(payload):
    # Check if the event is an 'updated.deal' event
    if 'event' in payload and payload['event'] == 'updated.deal':
        # Check if 'current' and 'previous' deal information is present
        if 'current' in payload and 'previous' in payload:
            current_stage_id = payload['current'].get('stage_id')
            previous_stage_id = payload['previous'].get('stage_id')

            # Check if the stage_id has changed
            if current_stage_id is not None and previous_stage_id is not None and current_stage_id != previous_stage_id:
                # Return the new stage_id
                print(f"New stage_id: {current_stage_id}")
                return current_stage_id

    # Return False if it wasn't a stage update
    return False