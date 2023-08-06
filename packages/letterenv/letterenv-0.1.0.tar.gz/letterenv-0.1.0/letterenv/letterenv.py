from itertools import product

import numpy as np
from gymnasium import Env, spaces

from letterenv.config import DefaultConfig, EnvironmentConfig


class LetterEnv(Env):
    """Letter environment."""

    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

    metadata = {"render_modes": ["ansi"], "render_fps": 1}

    def __init__(self, config: EnvironmentConfig = DefaultConfig()) -> None:
        super().__init__()

        # Setup environment configuation
        self.config = config
        self.prop_idx = {p: i for i, p in enumerate(self.config.propositions)}

        # Define environment spaces
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Tuple(
            spaces=(
                spaces.Discrete(self.config.n_rows),
                spaces.Discrete(self.config.n_cols),
                spaces.Text(
                    min_length=0,
                    max_length=1,
                    charset="".join(self.config.propositions + ["_"]),
                ),
            ),
        )
        self.reward_range = (0, 1)

    def reset(
        self,
        seed: int | None = None,
        options: dict | None = None,
    ):
        super().reset(seed=seed)
        # Reset number of steps taken in environment
        self.n_steps = 0

        # Set number of times each proposition has been observed to 0
        self.prop_obs_counts = np.zeros((len(self.config.propositions),))

        # Define active propositions for each environment location
        self.active_propositions = {pos: p for p, pos in self.config.locations.items()}

        # Set agent initial position
        self.agent_position = self.config.agent_start_location
        return self._construct_observation(), {}

    def step(self, action: int):
        # Move agent in environment
        self._update_agent_position(action)

        # Calculate which propositions are true in the environment
        if self.agent_position in self.active_propositions:
            obs_prop = self.active_propositions[self.agent_position]

            # Update number of times proposition has been observed
            prop_idx = self.prop_idx[obs_prop]
            self.prop_obs_counts[prop_idx] += 1

            if (
                self.prop_obs_counts[prop_idx]
                == self.config.max_observation_counts[obs_prop]
            ):
                # Replace proposition with next proposition in replacement mapping
                self.active_propositions[
                    self.agent_position
                ] = self.config.replacement_mapping[obs_prop]

        else:
            obs_prop = "_"

        # Determine all propositions have been observed the maximum number of times
        all_props_observed_max = True

        for oc, mc in zip(
            self.prop_obs_counts,
            self.config.max_observation_counts.values(),
        ):
            if mc is None:
                continue

            if oc < mc:
                all_props_observed_max = False
                break

        obs = self._construct_observation()

        # Determine if episode is terminated due to max number of steps
        if self.spec is not None and self.spec.max_episode_steps == self.n_steps:
            terminated = True
            # Episode ended based on condition outside MDP (interface for more details)
            truncated = True
            reward = 0
        else:
            terminated = all_props_observed_max
            truncated = False
            reward = 1 if terminated else 0

        return (
            obs,
            reward,
            terminated,
            truncated,
            {},
        )

    def render(self) -> str:
        """Render the environment as a string."""
        str_repr = ""

        for r in range(self.config.n_rows):
            for c in range(self.config.n_cols):
                if (r, c) == self.agent_position:
                    str_repr += "\x1b[1;37;42m" + "x" + "\x1b[0m" + " "
                elif (r, c) in self.active_propositions:
                    str_repr += self.active_propositions[(r, c)] + " "
                else:
                    str_repr += "." + " "
            str_repr += "\n"
        return str_repr

    def _update_agent_position(self, action: int) -> None:
        """Moves that take agent out of the grid leave it in the same position."""
        row, col = self.agent_position

        if action == self.RIGHT:
            n_row = row
            n_col = col + 1 if col < self.config.n_cols - 1 else col
        elif action == self.LEFT:
            n_row = row
            n_col = col - 1 if col > 0 else col
        elif action == self.UP:
            n_col = col
            n_row = row - 1 if row > 0 else row
        elif action == self.DOWN:
            n_col = col
            n_row = row + 1 if row < self.config.n_rows - 1 else row
        else:
            raise ValueError(f"Invalid action {action}.")
        self.agent_position = (n_row, n_col)

    def _construct_observation(self):
        if self.agent_position in self.active_propositions:
            obs_props = self.active_propositions[self.agent_position]
        else:
            obs_props = "_"

        return (
            self.agent_position[0],
            self.agent_position[1],
            obs_props,
        )
