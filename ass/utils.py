import sys

# this code looks like shit because
# 1) python has a design flaw this: http://stackoverflow.com/questions/5218895/python-nested-functions-variable-scoping
# 2) python does not have switches

TOKEN_NORMAL = 0
TOKEN_DBL_Q  = 1
TOKEN_SNG_Q  = 2

def tokenize(inp):
    _oldstate = {'state': TOKEN_NORMAL, 'lastStateChange': 0}
    i = 0
    tokens = []
    def state(newstate, oldstate, i):
        start = oldstate['lastStateChange']
        end   = i - 1
        if oldstate['state'] != TOKEN_NORMAL:
            start -= 1
            end += 1
        tokens.append({'type': oldstate['state'], 'token': inp[start:end]})
        oldstate['state'] = newstate
        oldstate['lastStateChange'] = i

    while i < len(inp):
        ch = inp[i]
        i += 1
        if ch == '\\':
            i += 1
            continue
        if _oldstate['state'] == TOKEN_NORMAL:
            if ch == '"':
                state(TOKEN_DBL_Q, _oldstate, i)
            elif ch == '\'':
                state(TOKEN_SNG_Q, _oldstate, i)
            pass
        elif _oldstate['state'] == TOKEN_DBL_Q:
            if ch == '"':
                state(TOKEN_NORMAL, _oldstate, i)
            pass
        elif _oldstate['state'] == TOKEN_SNG_Q:
            if ch == '\'':
                state(TOKEN_NORMAL, _oldstate, i)
            pass
        else:
            raise Exception('Well, shit.')
            break
    # end
    state(0xff, _oldstate, i + 1)
    return tokens