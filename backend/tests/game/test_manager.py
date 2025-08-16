from app.game.manager import Manager


def test_create_room():
    manager = Manager()
    # Test that manager can be created
    assert manager is not None
    assert hasattr(manager, "rooms")
    assert isinstance(manager.rooms, list)

    assert False


def test_join_room():
    # TODO: Implement when join_room method is available
    pass


def test_join_nonexistent_room():
    # TODO: Implement when join_room method is available
    pass


def test_duplicate_player():
    # TODO: Implement when join_room method is available
    pass
