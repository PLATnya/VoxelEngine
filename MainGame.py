from Engine import *
import Session

if __name__ == "__main__":
    main_session = Session.GameSession()
    main_session.add_event(CloseEvent())
    main_session.add_event(KeyEvent())
    main_session.add_event(KeyUpEvent())
    main_session.add_event(CameraMoveEvent())
    main_session.add_event(CameraRotateEvent())
    main_session.add_event(EscapeButtonExitEvent())



    main_session.add_event(ConstructMoveEvent(pg.K_KP6, np.array([-1, 0])))
    main_session.add_event(ConstructMoveEvent(pg.K_KP4, np.array([1, 0])))
    main_session.add_event(ConstructMoveEvent(pg.K_KP8, np.array([0, 1])))
    main_session.add_event(ConstructMoveEvent(pg.K_KP2, np.array([0, -1])))

    main_session.add_event(ConstructNewVoxelEvent(pg.K_KP5))
    main_session.add_event(DestroyNewVoxelEvent(pg.K_KP0))
    main_session.add_event(StepEvent())

    main_session.init_session()
    main_session.main_loop()
