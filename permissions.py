import config


def is_role_admin(role):
    role_is_admin = False
    for i in config.CONFIG["admin_prefixes"]:
        if role.name.startswith(i):
            role_is_admin = True
            break

    return role_is_admin


async def developer(ctx):
    if ctx.author.id not in config.CONFIG["developers"]:
        await ctx.send(content=":octagonal_sign: Cette commande requiert les privilèges développeur !", hidden=True)
        return False
    else:
        return True


async def admin(ctx):
    if ctx.author.id in config.CONFIG["developers"]:
        return True

    for role in ctx.author.roles:
        if is_role_admin(role):
            return True

    await ctx.send(content=":octagonal_sign: Vous n'êtes pas autorisé à utiliser cette commande !", hidden=True)
    return False
