from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import categories as category_crud
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.product import ProductResponse


router = APIRouter(
    prefix="/categories",
    tags=["Categorias"],
    responses={
        404: {"description": "Categoria não encontrada."},
        409: {"description": "A categoria não pode ser excluída enquanto possuir produtos."},
        422: {"description": "Os dados enviados são inválidos."},
    },
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar categoria",
    description="Cadastra uma categoria e retorna os dados criados.",
    response_description="Categoria criada.",
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    return category_crud.create_category(db, category_data)


@router.get(
    "",
    response_model=list[CategoryResponse],
    summary="Listar categorias",
    description="Retorna todas as categorias cadastradas.",
    response_description="Lista de categorias.",
)
def list_categories(db: Session = Depends(get_db)):
    return category_crud.get_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Consultar categoria",
    description="Retorna uma categoria pelo identificador.",
    response_description="Categoria encontrada.",
)
def read_category(
    category_id: int = Path(description="Identificador da categoria."),
    db: Session = Depends(get_db),
):
    category = category_crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return category


@router.get(
    "/{category_id}/products",
    response_model=list[ProductResponse],
    summary="Listar produtos da categoria",
    description="Retorna os produtos associados a uma categoria.",
    response_description="Lista de produtos da categoria.",
)
def list_category_products(
    category_id: int = Path(description="Identificador da categoria."),
    db: Session = Depends(get_db),
):
    category = category_crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return category_crud.get_products_for_category(category)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Atualizar categoria",
    description="Atualiza os dados de uma categoria existente.",
    response_description="Categoria atualizada.",
)
def update_category(
    category_data: CategoryUpdate,
    category_id: int = Path(description="Identificador da categoria."),
    db: Session = Depends(get_db),
):
    category = category_crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return category_crud.update_category(db, category, category_data)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir categoria",
    description="Exclui uma categoria somente se ela não possuir produtos.",
    response_description="Categoria excluída.",
)
def delete_category(
    category_id: int = Path(description="Identificador da categoria."),
    db: Session = Depends(get_db),
):
    category = category_crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    if category_crud.get_products_for_category(category):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir uma categoria que possui produtos.",
        )
    category_crud.delete_category(db, category)
