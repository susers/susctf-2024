package main

import (
	"bytes"
	"fmt"
	"html/template"

	"github.com/kataras/iris/v12"
)

var viewed bool
var option string = "URLParams"
var result string = "<nil>"

func main() {
	app := iris.New()

	tmpl := iris.HTML("./views", ".html")
	tmpl.Reload(true)
	app.RegisterView(tmpl)

	handleWebhook := func(ctx iris.Context) {
		var tmpl = fmt.Sprintf("<p> %s: <br> {{ range $k, $v := .%s }} {{ $k }}: {{ $v }} <br> {{ else }} Aughh! Nothing! {{ end }} </p>", option, option)
		tmpl += "\n<p> Body: <br> {{ printf \"%s\" .GetBody }} </p>"
		t, err := template.New("page").Parse(tmpl)
		if err != nil {
			ctx.StatusCode(iris.StatusInternalServerError)
			ctx.Text(err.Error())
			return
		}
		buf := new(bytes.Buffer)
		err = t.Execute(buf, ctx)
		if err != nil {
			ctx.StatusCode(iris.StatusInternalServerError)
			ctx.Text(err.Error())
			return
		}
		result = buf.String()
		ctx.StatusCode(iris.StatusOK)
		ctx.HTML(result)
		return
	}
	app.Get("/webhook", handleWebhook)
	app.Post("/webhook", handleWebhook)

	app.Post("/option", func(ctx iris.Context) {
		option = ctx.PostValueDefault("option", "URLParams")
		ctx.StatusCode(iris.StatusOK)
		ctx.Text("Success")
		return
	})

	app.Get("/", func(ctx iris.Context) {
		ctx.ViewData("result", template.HTML(result))
		err := ctx.View("index.html")
		if err != nil {
			ctx.StatusCode(iris.StatusInternalServerError)
			ctx.Text(err.Error())
			return
		}
		ctx.StatusCode(iris.StatusOK)
		result = "<nil>"
		return
	})

	// listen
	app.Listen(":8080")
}
