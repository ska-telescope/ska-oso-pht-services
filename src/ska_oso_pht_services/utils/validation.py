from ska_oso_pdm import Proposal

# from ska_oso_pht_services.api_clients.osd_api import osd_client

# TODO: use values from OSD after connection is ready


def validate_proposal(proposal: Proposal) -> dict:
    """
    validate proposal

    1. check that proposal has at least one obervation set
    2. each observation target should have a valid senscal result
    3. check that each observation sets has at least one target (in result)

    Parameters:
    proposal (Proposal): proposal to be validated

    Returns:
    dict: result of validation and messages
    """

    validate_result = True

    messages = []
    try:
        # check that proposal has at least one obervation set
        if len(proposal.info.observation_sets) == 0:
            validate_result = False
            messages.append("Proposal has no oberservation sets")

        # each observation target should have a valid senscal result
        for target in proposal.info.targets:
            if not any(
                target.target_id == result.target_ref
                for result in proposal.info.results
            ):
                validate_result = False
                messages.append(
                    f"Target {target.target_id} has no valid senscalc result"
                )

        # check that each observation sets has at least one target (in result)
        for obs_set in proposal.info.observation_sets:
            if not any(
                obs_set.observation_set_id == result.observation_set_ref
                for result in proposal.info.results
            ):
                validate_result = False
                messages.append(
                    f"Observation Set {obs_set.observation_set_id} has no Targets in"
                    " Results"
                )

    except ValueError as err:
        messages.append("Exception: " + str(err))
        return {"result": False, "validation_errors": messages}
    return {"result": validate_result, "validation_errors": messages}
