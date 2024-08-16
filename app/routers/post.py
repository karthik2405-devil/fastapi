from fastapi import FastAPI,Response, status,HTTPException,Depends,APIRouter
import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List,Optional
from database import get_db
router=APIRouter()
@router.get("/")
async def get_user():
    return {"message":"welcome!!!"}


@router.get("/posts", response_model=List[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ''
):
    posts_query = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip)

    posts = posts_query.all()
    
    return posts
@router.post("/posts/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)

async def create_posts(post :schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    # post_dict=post.dict()
    # post_dict['id']=randrange(0,100000)
    # print(post_dict)

    # my_posts.append(post.dict())

    
    
    # cursor.execute(""" INSERT INTO PUBLIC.PRODUCTS(name,subscription,price) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.name,post.subscription,post.price))
    # new_post=cursor.fetchone()
    # conn.commit()

    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    #**post.dict() simplies writing the upper line instead makes it easy to add more variables and easy to map the input from postgres
    print(current_user)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
# you are assigningn a dict from body (postman) to a variable named payload



@router.get("/posts/{id}",response_model=schemas.PostOut)

async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ''
):
    # post=db.query(models.Post).filter(models.Post.id==id).first()
    # posts_query=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    
    posts_query = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).first()

    posts = posts_query
    

    # cursor.execute(f"""Select * from public.products where id={id} """,id)
    # post_with_id=cursor.fetchone()
    # return {"post":post_with_id}
    
    
    # post=find_post(id)
    if not posts_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id :{id} was not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f'post with id :{id} was not found'}
    
    return posts

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def post_delete(id:int,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    if post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'not authorised to perform the action ')

    post_query.delete(synchronize_session=False)
    db.commit()
    return post  

    # cursor.execute(f"""delete from public.products where id={id} returning *""",id)
    # delete_post=cursor.fetchone()
    # conn.commit()

    # index=find_posts_delete(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
                            
    #     # return {"message":f'post with id {id} not found'}
    # my_posts.pop(index)
    # # print('post was successfully deleted')
    # # return {"message":'post was successfully deleted'}
    # # Can't return a statement / message when we used the status code
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/posts/{id}')
def update_post(id:int,post:schemas.PostUpdate,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    updated_post=db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    if post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'not authorised to perform the action ')

    updated_post.update(post.dict(),synchronize_session=False)
    
    db.commit()
    return updated_post.first()
    
    
    # cursor.execute(
    #     """
    #     UPDATE public.products 
    #     SET name = %s, subscription = %s, price = %s 
    #     WHERE id = %s
    #     RETURNING *
    #     """,
    #     (post.name, post.subscription, post.price, id)
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    

    # index=find_post_index(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    
    # post_dict=post.dict()
    # post_dict['id']=id
    # my_posts[index]=post_dict

    # return{"data":post_dict}


