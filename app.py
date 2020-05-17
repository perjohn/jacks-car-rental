import click

from policy_iteration import iterate_policy, JacksCarRentalSolver


@click.command()
def approximate_policy():
    solver = JacksCarRentalSolver()


if __name__ == '__main__':
    approximate_policy()
