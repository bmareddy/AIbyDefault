import Constants
from Get_similar_pages_for_question import get_similar_pages_for_sentence
from Get_similar_words_for_page import get_similar_pages, get_tags_for_page


def parse_command(command):
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(Constants.EXAMPLE_COMMAND)

     # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(Constants.COMMAND_HELP):
        response = "Command help called"
    elif command.startswith(Constants.COMMAND_TAG):
        input = command.replace(Constants.COMMAND_TAG, "", 1)
        response = get_tags_for_page(Constants.space, Constants.version, input)
    elif command.startswith(Constants.COMMAND_ANSWER):
        input = command.replace(Constants.COMMAND_ANSWER, "", 1)
        response = get_similar_pages_for_sentence(Constants.space, Constants.version, input)
    elif command.startswith(Constants.COMMAND_SIMILAR):
        input = command.replace(Constants.COMMAND_SIMILAR, "", 1)
        response = get_similar_pages(Constants.space, Constants.version, input)
    elif command.startswith(Constants.COMMAND_SWITCH_TO):
        input = command.replace(Constants.COMMAND_SWITCH_TO, "", 1)
        response = "Switching space to {}".format(input)
        Constants.space = input
    elif command.startswith(Constants.COMMAND_VERSION):
        input = command.replace(Constants.COMMAND_VERSION, "", 1)
        if (input == "weighted"):
            Constants.version = "_weighted"
            response = "Using {} version".format(input)
        else:
            Constants.version = ""
            response = "Using Normal version"
    return response or default_response