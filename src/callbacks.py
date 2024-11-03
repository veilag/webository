from aiogram.filters.callback_data import CallbackData


class RequestApproveCallback(CallbackData, prefix="request"):
    approve: bool
    request_id: int
