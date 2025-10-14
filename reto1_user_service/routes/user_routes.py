from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from typing import List
import bcrypt
import logging

from models.user import UserCreate, UserUpdate, UserResponse, UserInDB
from config.database import get_database

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


def hash_password(password: str) -> str:
    """Encripta la contraseña usando bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Crear un nuevo usuario.
    
    - **name**: Nombre completo del usuario
    - **email**: Email único del usuario
    - **password**: Contraseña (será encriptada con bcrypt)
    """
    try:
        db = get_database()
        
        # Verificar si el email ya existe
        existing_user = await db.users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user.email} already registered"
            )
        
        # Encriptar password
        hashed_password = hash_password(user.password)
        
        # Crear documento de usuario
        user_dict = {
            "name": user.name,
            "email": user.email,
            "hashed_password": hashed_password
        }
        
        # Insertar en MongoDB
        result = await db.users.insert_one(user_dict)
        
        # Obtener el usuario creado
        created_user = await db.users.find_one({"_id": result.inserted_id})
        
        logger.info(f"✅ User created successfully: {user.email}")
        
        return UserResponse(
            _id=str(created_user["_id"]),
            name=created_user["name"],
            email=created_user["email"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """
    Obtener un usuario por su ID.
    
    - **user_id**: ID único del usuario (ObjectId de MongoDB)
    """
    try:
        db = get_database()
        
        # Validar ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        # Buscar usuario
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        logger.info(f"✅ User retrieved: {user_id}")
        
        return UserResponse(
            _id=str(user["_id"]),
            name=user["name"],
            email=user["email"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error retrieving user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user: {str(e)}"
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    """
    Actualizar un usuario existente.
    
    - **user_id**: ID del usuario a actualizar
    - Todos los campos son opcionales
    """
    try:
        db = get_database()
        
        # Validar ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        # Verificar que el usuario existe
        existing_user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        # Preparar datos de actualización (solo campos no nulos)
        update_data = {}
        
        if user_update.name is not None:
            update_data["name"] = user_update.name
        
        if user_update.email is not None:
            # Verificar que el nuevo email no esté en uso por otro usuario
            email_exists = await db.users.find_one({
                "email": user_update.email,
                "_id": {"$ne": ObjectId(user_id)}
            })
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {user_update.email} already in use"
                )
            update_data["email"] = user_update.email
        
        if user_update.password is not None:
            update_data["hashed_password"] = hash_password(user_update.password)
        
        # Si no hay campos para actualizar
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Actualizar en MongoDB
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        # Obtener usuario actualizado
        updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
        
        logger.info(f"✅ User updated successfully: {user_id}")
        
        return UserResponse(
            _id=str(updated_user["_id"]),
            name=updated_user["name"],
            email=updated_user["email"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Eliminar un usuario.
    
    - **user_id**: ID del usuario a eliminar
    """
    try:
        db = get_database()
        
        # Validar ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        # Verificar que el usuario existe
        existing_user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        # Eliminar usuario
        await db.users.delete_one({"_id": ObjectId(user_id)})
        
        logger.info(f"✅ User deleted successfully: {user_id}")
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )
