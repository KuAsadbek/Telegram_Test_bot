from aiogram.fsm.state import StatesGroup,State

class UserStates(StatesGroup):
    #registration
    full_name = State()
    classes = State()
    classes2 = State()
    school = State()
    teacher = State()
    contact = State()
    yes = State()
    
    #certificate
    certificate = State()

    # answer
    cod = State()
    answer = State()

    # settings
    main = State()
    name = State()
    last = State()