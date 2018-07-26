import Constants
from Get_similar_pages_for_question import get_similar_pages_for_sentence

def parse_command(command):
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(Constants.EXAMPLE_COMMAND)

     # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(Constants.COMMAND_HELP):
        response = "Command help called"
    elif command.startswith(Constants.COMMAND_TAG):        
        response = "Command tag called"
    elif command.startswith(Constants.COMMAND_ANSWER):
        input = command.replace(Constants.COMMAND_ANSWER, "", 1)
        response = get_similar_pages_for_sentence(Constants.space, input)
    elif command.startswith(Constants.COMMAND_SIMILAR):
        response = "Command similar called"
    elif command.startswith(Constants.COMMAND_SWITCH_TO):
        input = command.replace(Constants.COMMAND_SWITCH_TO, "", 1)
        response = "Switching space to {}".format(input)
        Constants.space = input
    return response or default_response