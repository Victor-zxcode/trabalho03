from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import products as product_crud
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate


router = APIRouter(
    prefix="/products",
    tags=["Produtos"],
    responses={
        404: {"description": "Produto ou categoria não encontrados."},
        422: {"description": "Os dados enviados são inválidos."},
    },
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar produto",
    description="Cadastra um produto associado a uma categoria existente.",
    response_description="Produto criado.",
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
):
    if not product_crud.category_exists(db, product_data.category_id):
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return product_crud.create_product(db, product_data)


@router.get(
    "",
    response_model=list[ProductResponse],
    summary="Listar produtos",
    description="Retorna todos os produtos cadastrados.",
    response_description="Lista de produtos.",
)
def list_products(db: Session = Depends(get_db)):
    return product_crud.get_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Consultar produto",
    description="Retorna um produto pelo identificador.",
    response_description="Produto encontrado.",
)
def read_product(
    product_id: int = Path(description="Identificador do produto."),
    db: Session = Depends(get_db),
):
    product = product_crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Atualizar produto",
    description="Atualiza o nome do produto ou a categoria à qual pertence.",
    response_description="Produto atualizado.",
)
def update_product(
    product_data: ProductUpdate,
    product_id: int = Path(description="Identificador do produto."),
    db: Session = Depends(get_db),
):
    product = product_crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    update_data = product_data.model_dump(exclude_unset=True)
    category_id = update_data.get("category_id")
    if category_id is not None and not product_crud.category_exists(db, category_id):
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return product_crud.update_product(db, product, product_data)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir produto",
    description="Exclui um produto pelo identificador.",
    response_description="Produto excluído.",
)
def delete_product(
    product_id: int = Path(description="Identificador do produto."),
    db: Session = Depends(get_db),
):
    product = product_crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    product_crud.delete_product(db, product)
