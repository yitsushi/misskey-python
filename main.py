import click
from Misskey import Client, Permissions


def display_note(note):
    user = note["user"]
    click.echo(f'[{note["id"]}] {user["name"]} '
               f'{user["username"]}@{user["host"]} '
               f'{note["createdAt"]}')
    click.echo(note['text'])
    if 'uri' in note:
        click.echo(f"  % {note['uri']}")
    else:
        click.echo(f"  % https://slippy.xyz/notes/{note['id']}")
    click.echo(f"Reactions: {note['reactions']}")
    click.echo(f"Emojies: {note['emojis']}")
    click.echo(f"Files: {note['files']}")
    click.echo("-" * 40)


def print_error(error):
    cargs = {'fg': 'red', 'err': True}
    click.secho(f'!!!!', **cargs)
    click.secho(f'[{error["code"]}] {error["message"]}', **cargs)
    click.secho(f'!!!!', **cargs)
    return


@click.group()
@click.option('--api-key', required=True, prompt=True, hide_input=True)
@click.pass_context
def cli(ctx, api_key):
    ctx.obj['client'] = Client('slippy.xyz', api_key)


@cli.group()
def admin():
    pass


@admin.group()
def queue():
    pass


@queue.command()
@click.pass_context
def jobs(ctx):
    client: Client = ctx.obj['client']
    queue = client.admin().queue().jobs('inbox', 'delayed')

    if 'error' in queue:
        error = queue['error']
        print_error(error)
        return

    for item in queue:
        activity = item["data"]["activity"]
        click.echo(f'[{item["id"]:<5s}] '
                   f'[{item["attempts"]}/{item["maxAttempts"]}] '
                   f'{activity["type"]} {activity["actor"]}')


@cli.command()
@click.option('--limit', default=10)
@click.pass_context
def notes(ctx, limit):
    client: Client = ctx.obj['client']
    note_list = client.notes(limit=10, reply=False, renote=True)

    if 'error' in note_list:
        error = note_list['error']
        print_error(error)
        return

    for note in note_list:
        if note['renote'] is not None:
            display_note(note['renote'])
        else:
            display_note(note)


@cli.group()
def app():
    pass


@app.command()
@click.option('--name', '-n', required=True)
@click.option('--description', '-d', required=True)
@click.option('--permission', '-p', multiple=True, required=True)
@click.option('--callback-url')
@click.pass_context
def create(ctx, name, description, permission, callback_url):
    permission = list(permission)
    if 'all' in permission:
        permission += Permissions().all()
        permission.remove('all')
    if 'all_read' in permission:
        permission += Permissions().all_read()
        permission.remove('all_read')
    if 'all_write' in permission:
        permission += Permissions().all_write()
        permission.remove('all_write')

    permission = list(set(permission))

    if any([not Permissions().is_valid(x) for x in permission]):
        cargs = {'err': True}
        click.secho("Some of the permissions are not valid", fg='red', **cargs)
        click.echo("Available permissions:", **cargs)
        click.echo("  Aliases:", **cargs)
        click.echo("    all       -> all permissions", **cargs)
        click.echo("    all_read  -> all read permissions", **cargs)
        click.echo("    all_write -> all write permissions", **cargs)
        click.echo("  READ:", **cargs)
        rperms = Permissions().all_read()
        click.echo("\n".join([f'    {x}' for x in rperms]), **cargs)
        click.echo("  WRITE:", **cargs)
        wperms = Permissions().all_write()
        click.echo("\n".join([f'    {x}' for x in wperms]), **cargs)
        return

    client: Client = ctx.obj['client']
    response = client.app().create(name, description, permission, callback_url)

    if 'error' in response:
        error = response['error']
        print_error(error)
        return

    click.echo(f'ID: {response["id"]}')
    click.echo(f'Name: {response["name"]}')
    click.echo(f'Callback URL: {response["callbackUrl"]}')
    click.echo('---')
    click.echo(f'Secret: {response["secret"]}')


if __name__ == '__main__':
    cli(obj={}, auto_envvar_prefix='MISSKEY')
