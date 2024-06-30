import enact
import random

@enact.register
def roll_die(sides: int) -> int:
  """Roll a die."""
  return random.randint(1, sides)

@enact.register
def roll_sum(num_rolls: int) -> int:
  """Roll dice."""
  return sum(roll_die(6) for _ in range(num_rolls))

with enact.InMemoryStore() as store:
  invocation = enact.invoke(roll_sum, (2,))
  print(enact.invocation_summary(invocation))

# Rewind the last roll and replay it.
with store:
  first_roll = invocation.rewind(1)    # Rewind by one roll.
  print('Partial invocation: ')
  print(enact.invocation_summary(first_roll))
  reroll_second = first_roll.replay()  # Replay the second die roll.
  print('\nReplayed invocation: ')
  print(enact.invocation_summary(reroll_second))
