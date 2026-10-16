from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryCreate(BaseModel):
    model_config = ConfigDict(title="Dados para criação de categoria")

    name: str = Field(
        title="Nome",
        min_length=1,
        max_length=100,
        description="Nome da categoria.",
        examples=["Informática"],
    )


class CategoryUpdate(BaseModel):
    model_config = ConfigDict(title="Dados para atualização de categoria")

    name: str | None = Field(
        default=None,
        title="Nome",
        min_length=1,
        max_length=100,
        description="Novo nome da categoria.",
        examples=["Eletrônicos"],
    )

    @field_validator("name", mode="before")
    @classmethod
    def reject_null_name(cls, value):
        if value is None:
            raise ValueError("O nome não pode ser nulo.")
        return value


class CategoryResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        title="Categoria retornada pela API",
    )

    id: int = Field(title="Identificador", description="Identificador da categoria.")
    name: str = Field(title="Nome", description="Nome da categoria.")
