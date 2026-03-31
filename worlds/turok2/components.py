from worlds.LauncherComponents import Component, Type, components, launch, icon_paths

def run_client(*args: str) -> None:
    '''
    Runs the client, which will run our bridge to communicate with the game.
    This is set up below to be ran when launched from the AP client.
    '''
    from .client.launch import launch_ap_turok2_client
    launch(launch_ap_turok2_client, name="Turok 2 Client", args=args)

# Defines the component. The function in func will be ran when the game is launched from the AP client.
icon_paths["turok2"] = f"ap:{__name__}/icons/turok2.png"
components.append(
    Component(
        "Turok 2 Client",
        func=run_client,
        game_name="Turok 2",
        component_type=Type.CLIENT,
        supports_uri=True,
        icon="turok2",
    )
)
