import click

from policy_iteration import JacksCarRentalSolver


@click.command()
def approximate_policy():
    solver = JacksCarRentalSolver()
    solver.policy_evaluation()


if __name__ == '__main__':
    approximate_policy()
