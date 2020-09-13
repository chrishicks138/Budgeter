from app import app
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    HiddenField,
    SelectField,
)
from wtforms.validators import DataRequired
from flask import render_template, redirect, url_for
import os
from app.models import Expense, Income
from app import db
import app.Occurence_class as Occurence
import app.Dates as Dates

expenses = []
prices = []
occurences = []
incomes = []
income_prices = []
income_occurences = []
date_list = Dates.Comprehensions().d
dates = Dates.Dates()


class SpanForm(FlaskForm):
    span = SelectField(
        "Span",
        default="1",
        choices=[
            ("1", "1 Week"),
            ("2", "2 Weeks"),
            ("3", "1 Month"),
            ("4", "3 Months"),
            ("5", "6 Months"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Select Span Scheme")


class IncomeForm(FlaskForm):
    income = StringField("income", validators=[DataRequired()])
    price = StringField("price", validators=[DataRequired()])
    occurence = SelectField(
        "occurence",
        choices=[
            ("1", "Daily"),
            ("2", "Weekly"),
            ("3", "Every other day"),
            ("4", "Biweekly"),
            ("5", "Existing balance"),
        ],
        validators=[DataRequired()],
    )
    days = date_list
    print(days)
    payday = SelectField(
        "payday",
        choices=[
            ("0", days[0]),
            ("1", days[1]),
            ("2", days[2]),
            ("3", days[3]),
            ("4", days[4]),
            ("5", days[5]),
            ("6", days[6]),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Add Income")


class deleteIncomeForm(FlaskForm):
    hidden = HiddenField("", validators=[DataRequired()])
    submit = SubmitField("Delete")


class deleteExpenseForm(FlaskForm):
    hidden = HiddenField("", validators=[DataRequired()])
    submit = SubmitField("Delete")


class ExpenseForm(FlaskForm):
    expense = StringField("expense", validators=[DataRequired()])
    price = StringField("price", validators=[DataRequired()])
    occurence = SelectField(
        "occurence",
        choices=[("1", "Daily"),
                 ("2", "Weekly"),
                 ("3", "Every other day"),
                 ("4", "Biweekly")],
        validators=[DataRequired()],
    )
    expenseDate = SelectField(
        "expenseDate",
        choices=[
            ("0", "Sunday"),
            ("1", "Monday"),
            ("2", "Tuesday"),
            ("3", "Wednesday"),
            ("4", "Thursday"),
            ("5", "Friday"),
            ("6", "Saturday"),
        ],
    )
    submit = SubmitField("Add Expense")


def db_commit():
    db.session.commit()
    return redirect("/")


def form_submit(expense_form, income_form):
    if expense_form.validate_on_submit():
        expense = Expense(
            expense=expense_form.expense.data,
            price=expense_form.price.data,
            occurence=expense_form.occurence.data,
            expenseDate=expense_form.expenseDate.data
        )
        db.session.add(expense)
        db_commit()

    if income_form.validate_on_submit():
        income = Income(
            income=income_form.income.data,
            price=income_form.price.data,
            occurence=income_form.occurence.data,
            payday=income_form.payday.data,
        )
        db.session.add(income)
        db_commit()


@app.route("/", methods=["GET", "POST"])
def chart():
    # Dates.Now().start()
    income_list = Income.query.all()
    expense_list = Expense.query.all()
    deleteIncome = deleteIncomeForm()
    deleteExpense = deleteExpenseForm()
    expense_form = ExpenseForm()
    income_form = IncomeForm()
    span_form = SpanForm()
    form_submit(expense_form, income_form)
    span = span_form.span.data
    if span == "1":
        span_label = '7'
    if span == "2":
        span_label = '14'
    if span == "3":
        span_label = '31'
    if span == "4":
        span_label = '90'
    if span == "5":
        span_label = '180'
    legend = "Daily Balance"
    dates.date_selector(span)
    labels, values, days = Occurence.Occurence().range_calc(span)
    # Dates.Now().end()
    # print(Dates.Now().result())
    return render_template(
        "chart.html",
        span=span_form,
        deleteExpense=deleteExpense,
        expenses=expense_list,
        incomes=income_list,
        deleteIncome=deleteIncome,
        income_form=income_form,
        expense_form=expense_form,
        values=values,
        labels=labels,
        days=days,
        legend=legend,
        span_label=span_label,
    )


@app.route("/delete_expense", methods=["GET", "POST"])
def delete_expense():
    deleteExpense = deleteExpenseForm()
    if deleteExpense.is_submitted():
        e = Expense.query.get(deleteExpense.hidden.data)
        db.session.delete(e)
        db_commit()
    return redirect("/")


@app.route("/delete_income", methods=["GET", "POST"])
def delete_income():
    deleteIncome = deleteIncomeForm()
    if deleteIncome.is_submitted():
        i = Income.query.get(deleteIncome.hidden.data)
        db.session.delete(i)
        db_commit()
    return redirect("/")


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)