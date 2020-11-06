
def ask_yn_q(question):
  question = question+' '
  resp = input(question).strip().lower()
  while resp[0] != 'y' and resp[0] != 'n':
    print("Please answer 'yes' or 'no' ('y' and 'n' are also accepted)")
    resp = input(question).strip().lower()
  # True if 'y' False if 'n'
  return resp[0] == 'y'

