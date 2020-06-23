import os

import click
import numpy as np

from policy_iteration import JacksCarRentalSolver


@click.command()
@click.option('--root-dir', type=click.Path(exists=True), help='Directory to save temporary results')
def approximate_policy(root_dir):
    solver = JacksCarRentalSolver()
    policy_stable = False
    loop_count = 1
    while not policy_stable:
        print(f'Policy approximation loop {loop_count}')
        solver.policy_evaluation()
        if root_dir:
            np.save(os.path.join(root_dir, f'jacks-car-rental-values-{loop_count}.npy'), solver.values)
        policy_stable = solver.policy_improvement()
        if root_dir:
            np.save(os.path.join(root_dir, f'jacks-car-rental-policy-{loop_count}.npy'), solver.values)
        loop_count += 1


if __name__ == '__main__':
    approximate_policy()
