Common libs for Memolife services
=========================

Add it to your project:

    pip install -e git+ssh://git@github.com/Memolife/service-common.git#egg=memolife

And use it:

   from memolife import auth

   @auth.is_authenticated
   def foo():
       return make_response("", 200)


