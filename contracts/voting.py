from pyteal import *

def approval_program():
    counter = Bytes("counter")

    # On application creation
    on_create = Seq(
        App.globalPut(counter, Int(0)),
        Return(Int(1))
    )

    # On NoOp call: increment counter
    on_increment = Seq(
        App.globalPut(counter, App.globalGet(counter) + Int(1)),
        Return(Int(1))
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, on_increment]
    )

    return program


def clear_state_program():
    return Return(Int(1))


if __name__ == "__main__":
    print(compileTeal(approval_program(), Mode.Application, version=6))
