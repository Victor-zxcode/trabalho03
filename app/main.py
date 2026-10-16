from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import categories, products


def translate_validation_message(error: dict[str, Any]) -> str:
    error_type = error["type"]
    context = error.get("ctx", {})

    if error_type == "missing":
        return "Este campo é obrigatório."
    if error_type == "string_too_short":
        minimum = context.get("min_length")
        unit = "caractere" if minimum == 1 else "caracteres"
        return f"Informe pelo menos {minimum} {unit}."
    if error_type == "string_too_long":
        return f"Informe no máximo {context.get('max_length')} caracteres."
    if error_type == "greater_than":
        return f"Informe um valor maior que {context.get('gt')}."
    if error_type in {"int_parsing", "int_type"}:
        return "Informe um número inteiro válido."
    if error_type == "string_type":
        return "Informe um texto válido."
    if error_type == "json_invalid":
        return "O corpo da requisição deve conter um JSON válido."
    if error_type == "value_error":
        validation_error = context.get("error")
        if validation_error is not None:
            return str(validation_error)
    return "O valor informado para este campo é inválido."


app = FastAPI(
    title="API de Categorias e Produtos",
    summary="Cadastro e consulta de categorias e produtos",
    description=(
        "API para cadastrar e consultar categorias e produtos. "
        "Cada produto pertence a uma categoria existente."
    ),
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Categorias",
            "description": "Operações para cadastrar, consultar, atualizar e excluir categorias.",
        },
        {
            "name": "Produtos",
            "description": "Operações para cadastrar, consultar, atualizar e excluir produtos.",
        },
    ],
)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    del request
    errors = jsonable_encoder(exc.errors())
    for error in errors:
        error["msg"] = translate_validation_message(error)
    return JSONResponse(status_code=422, content={"detail": errors})


app.include_router(categories.router)
app.include_router(products.router)
