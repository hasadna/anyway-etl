import click


@click.group()
def cbs():
    pass


@cbs.command()
def import_emails():
    """Retrieve cbs emails from imap and save to a datapackage"""
    from . import import_emails
    import_emails.main()


@cbs.command()
def process_files():
    """Extract and process the cbs files"""
    from . import process_files
    process_files.main()


@cbs.command()
@click.option('--load-start-year')
def import_to_datastore(**kwargs):
    """Import the data from yearly directories to the DB"""
    from . import import_to_datastore
    import_to_datastore.main(**kwargs)


@cbs.command()
@click.option('--load-start-year')
def parse_accidents(**kwargs):
    """Parse the accident markers from yearly directories to datapackage"""
    from . import parse_accidents
    parse_accidents.main(**kwargs)


@cbs.command()
@click.option('--load-start-year')
def parse_involved(**kwargs):
    """Parse the involved from yearly directories to datapackage"""
    from . import parse_involved
    parse_involved.main(**kwargs)


@cbs.command()
@click.option('--load-start-year')
def parse_vehicles(**kwargs):
    """Parse the vehicles from yearly directories to datapackage"""
    from . import parse_vehicles
    parse_vehicles.main(**kwargs)


@cbs.command()
@click.option('--load-start-year')
def parse_all(**kwargs):
    from . import parse_vehicles, parse_accidents, parse_involved
    print("Parsing accidents...")
    parse_accidents.main(**kwargs)
    print("Parsing vehicles...")
    parse_vehicles.main(**kwargs)
    print("Parsing involved...")
    parse_involved.main(**kwargs)


@cbs.command()
@click.option('--last-update-ttl-days', type=int, default=90)
def check_data_in_datastore(**kwargs):
    from . import check_data_in_datastore
    exit(0 if check_data_in_datastore.main(**kwargs) else 1)
