import enact
import random

@enact.register
def human_rolls_die():
  """Query the user for a die roll."""
  return enact.request_input(requested_type=int, for_value='Please roll a die.')

@enact.register
def roll_dice_user_flow():
  """Request the number of die to roll and optionally sample die rolls."""
  num_rolls = enact.request_input(requested_type=int, for_value='Total number of rolls?')
  return sum(human_rolls_die() for _ in range(num_rolls))

request_responses = {
  'Total number of rolls?': 3,  # Roll 3 dice.
  'Please roll a die.': 6,      # Humans always roll 6.
}

with enact.InMemoryStore() as store:
  invocation_gen = enact.InvocationGenerator.from_callable(
    roll_dice_user_flow)
  # Process all user input requests in order.
  for input_request in invocation_gen:
    invocation_gen.set_input(request_responses[input_request.for_value()])
  print(enact.invocation_summary(invocation_gen.invocation))
