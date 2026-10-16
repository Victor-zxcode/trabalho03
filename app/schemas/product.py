from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    model_config = ConfigDict(title="Dados para criação de produto")

    name: str = Field(
        title="Nome",
        min_length=1,
        max_length=100,
        description="Nome do produto.",
        examples=["Teclado"],
    )
    category_id: int = Field(
        title="Identificador da categoria",
        gt=0,
        description="Identificador de uma categoria existente.",
        examples=[1],
    )


class ProductUpdate(BaseModel):
    model_config = ConfigDict(title="Dados para atualização de produto")

    name: str | None = Field(
        default=None,
        title="Nome",
        min_length=1,
        max_length=100,
        description="Novo nome do produto.",
        examples=["Teclado sem fio"],
    )
    category_id: int | None = Field(
        default=None,
        title="Identificador da categoria",
        gt=0,
        description="Identificador de uma categoria existente.",
        examples=[1],
    )

    @field_validator("name", "category_id", mode="before")
    @classmethod
    def reject_null_values(cls, value):
        if value is None:
            raise ValueError("Este campo não pode ser nulo.")
        return value


class ProductResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        title="Produto retornado pela API",
    )

    id: int = Field(title="Identificador", description="Identificador do produto.")
    name: str = Field(title="Nome", description="Nome do produto.")
    category_id: int = Field(
        title="Identificador da categoria",
        description="Identificador da categoria do produto.",
    )
