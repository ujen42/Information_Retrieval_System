from flask.views import MethodView
from flask import render_template, redirect, request
from utils.search import Search


class Home(MethodView):
    def get(self):
        return render_template("main/index.html")
    
    def post(self):
        form_data = request.form
        query = form_data.get('query')
        return redirect(f"/result?query={query}")


class ResultPage(MethodView):
    def get(self):
        query = request.args.get('query')
        if(query is None): return redirect('/')
        search = Search(query)
        result = search.search()
        return render_template("main/resultpage.html", query=query, result = result)

