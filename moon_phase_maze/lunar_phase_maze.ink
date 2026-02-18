=== beginning_room ===

You stand in the beginning room of an ink maze.
The only way forward is to follow the proper sequence.

* [Open the New Moon door.] -> phase_new_moon
* [Open the Waning Gibbous door.] -> dead_beginning_2_waning_gibbous
* [Open the Full Moon door.] -> dead_beginning_3_full_moon

=== phase_new_moon ===

You are in chamber 1 of 8.
An inscription on the wall reads: New Moon.
Three inked doors pulse with lunar light.

* [Choose Waning Gibbous.] -> dead_new_moon_1_waning_gibbous
* [Choose Waning Crescent.] -> dead_new_moon_2_waning_crescent
* [Choose Waxing Crescent.] -> phase_waxing_crescent

=== phase_waxing_crescent ===

You are in chamber 2 of 8.
An inscription on the wall reads: Waxing Crescent.
Three inked doors pulse with lunar light.

* [Choose Waning Gibbous.] -> dead_waxing_crescent_2_waning_gibbous
* [Choose First Quarter.] -> phase_first_quarter
* [Choose Waning Crescent.] -> dead_waxing_crescent_1_waning_crescent

=== phase_first_quarter ===

You are in chamber 3 of 8.
An inscription on the wall reads: First Quarter.
Three inked doors pulse with lunar light.

* [Choose Full Moon.] -> dead_first_quarter_2_full_moon
* [Choose Waxing Gibbous.] -> phase_waxing_gibbous
* [Choose New Moon.] -> dead_first_quarter_1_new_moon

=== phase_waxing_gibbous ===

You are in chamber 4 of 8.
An inscription on the wall reads: Waxing Gibbous.
Three inked doors pulse with lunar light.

* [Choose New Moon.] -> dead_waxing_gibbous_1_new_moon
* [Choose Full Moon.] -> phase_full_moon
* [Choose Waning Gibbous.] -> dead_waxing_gibbous_2_waning_gibbous

=== phase_full_moon ===

You are in chamber 5 of 8.
An inscription on the wall reads: Full Moon.
Three inked doors pulse with lunar light.

* [Choose Waxing Gibbous.] -> dead_full_moon_2_waxing_gibbous
* [Choose Waning Gibbous.] -> phase_waning_gibbous
* [Choose Full Moon.] -> dead_full_moon_1_full_moon

=== phase_waning_gibbous ===

You are in chamber 6 of 8.
An inscription on the wall reads: Waning Gibbous.
Three inked doors pulse with lunar light.

* [Choose Full Moon.] -> dead_waning_gibbous_1_full_moon
* [Choose Last Quarter.] -> phase_last_quarter
* [Choose New Moon.] -> dead_waning_gibbous_2_new_moon

=== phase_last_quarter ===

You are in chamber 7 of 8.
An inscription on the wall reads: Last Quarter.
Three inked doors pulse with lunar light.

* [Choose New Moon.] -> dead_last_quarter_1_new_moon
* [Choose Last Quarter.] -> dead_last_quarter_2_last_quarter
* [Choose Waning Crescent.] -> phase_waning_crescent

=== phase_waning_crescent ===

You are in chamber 8 of 8.
An inscription on the wall reads: Waning Crescent.
Three inked doors pulse with lunar light.

* [Open the exit archway] -> ending_room
* [Choose New Moon.] -> dead_waning_crescent_2_new_moon
* [Choose Full Moon.] -> dead_waning_crescent_1_full_moon

=== ending_room ===

You step into the ending room. Moonlight reflects on wet ink and resolves into dawn.

* [Breathe in relief.] -> DONE
* [Mark the maze as solved.] -> DONE
* [Step into daylight.] -> DONE

=== dead_beginning_2_waning_gibbous ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Waning Gibbous' when the maze demanded the next step after 'the beginning'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> beginning_room
* [Follow the narrow passage back.] -> beginning_room
* [Return to the previous chamber.] -> beginning_room

=== dead_beginning_3_full_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Full Moon' when the maze demanded the next step after 'the beginning'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> beginning_room
* [Follow the narrow passage back.] -> beginning_room
* [Return to the previous chamber.] -> beginning_room

=== dead_new_moon_1_waning_gibbous ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Waning Gibbous' when the maze demanded the next step after 'New Moon'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_new_moon
* [Follow the narrow passage back.] -> phase_new_moon
* [Return to the previous chamber.] -> phase_new_moon

=== dead_new_moon_2_waning_crescent ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Waning Crescent' when the maze demanded the next step after 'New Moon'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_new_moon
* [Follow the narrow passage back.] -> phase_new_moon
* [Return to the previous chamber.] -> phase_new_moon

=== dead_waxing_crescent_1_waning_crescent ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Waning Crescent' when the maze demanded the next step after 'Waxing Crescent'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_waxing_crescent
* [Follow the narrow passage back.] -> phase_waxing_crescent
* [Return to the previous chamber.] -> phase_waxing_crescent

=== dead_waxing_crescent_2_waning_gibbous ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Waning Gibbous' when the maze demanded the next step after 'Waxing Crescent'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_waxing_crescent
* [Follow the narrow passage back.] -> phase_waxing_crescent
* [Return to the previous chamber.] -> phase_waxing_crescent

=== dead_first_quarter_1_new_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'New Moon' when the maze demanded the next step after 'First Quarter'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_first_quarter
* [Follow the narrow passage back.] -> phase_first_quarter
* [Return to the previous chamber.] -> phase_first_quarter

=== dead_first_quarter_2_full_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Full Moon' when the maze demanded the next step after 'First Quarter'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_first_quarter
* [Follow the narrow passage back.] -> phase_first_quarter
* [Return to the previous chamber.] -> phase_first_quarter

=== dead_waxing_gibbous_1_new_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'New Moon' when the maze demanded the next step after 'Waxing Gibbous'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_waxing_gibbous
* [Follow the narrow passage back.] -> phase_waxing_gibbous
* [Return to the previous chamber.] -> phase_waxing_gibbous

=== dead_waxing_gibbous_2_waning_gibbous ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Waning Gibbous' when the maze demanded the next step after 'Waxing Gibbous'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_waxing_gibbous
* [Follow the narrow passage back.] -> phase_waxing_gibbous
* [Return to the previous chamber.] -> phase_waxing_gibbous

=== dead_full_moon_1_full_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Full Moon' when the maze demanded the next step after 'Full Moon'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_full_moon
* [Follow the narrow passage back.] -> phase_full_moon
* [Return to the previous chamber.] -> phase_full_moon

=== dead_full_moon_2_waxing_gibbous ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Waxing Gibbous' when the maze demanded the next step after 'Full Moon'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_full_moon
* [Follow the narrow passage back.] -> phase_full_moon
* [Return to the previous chamber.] -> phase_full_moon

=== dead_waning_gibbous_1_full_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Full Moon' when the maze demanded the next step after 'Waning Gibbous'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_waning_gibbous
* [Follow the narrow passage back.] -> phase_waning_gibbous
* [Return to the previous chamber.] -> phase_waning_gibbous

=== dead_waning_gibbous_2_new_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'New Moon' when the maze demanded the next step after 'Waning Gibbous'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_waning_gibbous
* [Follow the narrow passage back.] -> phase_waning_gibbous
* [Return to the previous chamber.] -> phase_waning_gibbous

=== dead_last_quarter_1_new_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'New Moon' when the maze demanded the next step after 'Last Quarter'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_last_quarter
* [Follow the narrow passage back.] -> phase_last_quarter
* [Return to the previous chamber.] -> phase_last_quarter

=== dead_last_quarter_2_last_quarter ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Last Quarter' when the maze demanded the next step after 'Last Quarter'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_last_quarter
* [Follow the narrow passage back.] -> phase_last_quarter
* [Return to the previous chamber.] -> phase_last_quarter

=== dead_waning_crescent_1_full_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'Full Moon' when the maze demanded the next step after 'Waning Crescent'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_waning_crescent
* [Follow the narrow passage back.] -> phase_waning_crescent
* [Return to the previous chamber.] -> phase_waning_crescent

=== dead_waning_crescent_2_new_moon ===

The door seals behind you. The room is silent and the ink dries to stone.
You followed 'New Moon' when the maze demanded the next step after 'Waning Crescent'.
A narrow passage opens behind you. You can turn around and try again.

* [Turn around and retrace your steps.] -> phase_waning_crescent
* [Follow the narrow passage back.] -> phase_waning_crescent
* [Return to the previous chamber.] -> phase_waning_crescent

-> beginning_room
