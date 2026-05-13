# FSRS Helper Data

## Dynamic Desired Retention Read

During rescheduling, FSRS Helper reads the deck/preset desired retention as the
base value. If the optional Dynamic Desired Retention add-on is available, FSRS
Helper calls `dynamic_desired_retention.effective_desired_retention()` with the
current collection, card and base desired retention.

If the optional add-on is missing, does not expose the resolver, returns `None`,
or raises an error, FSRS Helper keeps the base deck/preset desired retention.

## Reschedule Card Update

When a review card is rescheduled, FSRS Helper writes the desired retention used
for the calculation back to `card.desired_retention`, updates the card interval
and due date, and marks custom data key `v` as `reschedule`.
