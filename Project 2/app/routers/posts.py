from .. import model,schemas,utils
from fastapi import status,Response,HTTPException,APIRouter,Depends
from ..database import con,cursor
from sqlalchemy.orm import Session
from .. import oauth2
router=APIRouter(prefix='/posts')
@router.get("/")
def get_posts():
    cursor.execute("""select * from post""")
    posts=cursor.fetchall()
    print(posts)
    return {"data":posts}

@router.post("/",status_code=status.HTTP_201_CREATED)
def add_posts(response:Response,post:schemas.Post,current_user:int=Depends(oauth2.get_current_user)):
    print(current_user.email)
    cursor.execute("""insert into post(title,content,published) values (%s,%s,%s) returning *""",(post.title,post.content,post.published))
    post=cursor.fetchone()
    con.commit()
    return {"data":post}

@router.get("/{id}")
def get_post(id:int,current_user:int=Depends(oauth2.get_current_user)):
    cursor.execute("""select * from post where id=%s """,(str(id)))
    post =cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return {"data":post}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,current_user:int=Depends(oauth2.get_current_user)):
    cursor.execute("""delete from post where id=%s returning *""",(str(id)))
    post=cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No post found with id {id}")
    con.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id:int,post:schemas.Post,current_user:int=Depends(oauth2.get_current_user)):
    cursor.execute("update post set title=%s,content=%s,published=%s where id=%s returning *",(post.title,post.content,post.published,str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no post with id {id} found")
    con.commit()
    return {"data":post}