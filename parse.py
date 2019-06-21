from set_grammar import MARKER


class ParseResult:
    def __init__(self, is_correct, result, err_message = ''):
        self.is_correct = is_correct
        self.result = result
        self.err_message = err_message

    def __repr__(self):
        if self.err_message != '':
            return str(self.result) + " - " + str(self.err_message)
        else:
            return str(self.result)


def parse(tokens, all_tokens, relations):
    tokens = enumerate(tokens + [MARKER])
    error = ""
    result = []
    next_token_no, next_token = next(tokens)
    stack_tail, stack_head = [], MARKER
    while True:
        if next_token in all_tokens:
            print(" in stack_head / next_token: ", stack_head, '/', next_token)
            if stack_head == MARKER and next_token == MARKER:
                break
            relation = relations[stack_head][next_token]
            print ("relation = ", relation)
            if relation in ('<', '='):
                stack_tail.append(stack_head)
                stack_head = next_token
                next_token_no, next_token = next(tokens)
                continue
            if relation == '>':
                while True:
                    if stack_head not in ('(', ')'):
                        result.append(stack_head)
                    old_stack_head = stack_head
                    stack_head = stack_tail.pop()
                    if relations[stack_head][old_stack_head] == '<':
                        break
                continue
            else:
                error = "Error relationship"
        else:
            error = "Not found in All possible tokens"
        return ParseResult(False, f"Error in {next_token_no} token: '{next_token}'", error)

    return ParseResult(True, " ".join(result))
