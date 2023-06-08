import plotly.express as px


def plot_portfolio_total(temp_df,
                         account_names,
                         theme):
    temp_df.sort_values('date', inplace=True)
    fig = px.line(temp_df,
                  x='date',
                  y=temp_df[['total_value', 'total_investment_value']].columns,
                  title="Total portfolio values of '" + ",".join(account_names) + "' combined",
                  markers=True)
    fig.update_traces(connectgaps=True)
    fig.update_layout(
        template=theme,
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            tickvals=temp_df.date,
        ),

    )
    return fig


def plot_portfolio_all(df, theme, skip_zero=True):
    temp_df = df.drop('account_name', axis=1)

    if skip_zero:
        temp_df = temp_df.drop('date', axis=1)
        temp_df = temp_df.loc[:, (temp_df.sum(axis=0) != 0.0)]
        temp_df['date'] = df[['date']]

    fig = px.line(temp_df,
                  x=temp_df.date,
                  y=temp_df.columns,
                  title="All items",
                  markers=True)
    fig.update_traces(connectgaps=True)
    fig.update_layout(
        template=theme,
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            tickvals=df.date,
        ),

    )
    return fig
