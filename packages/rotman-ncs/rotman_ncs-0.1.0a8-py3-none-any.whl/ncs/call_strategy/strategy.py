from ..data import *
import pandas as pd
import numpy as np
import plotly.express as px
from IPython.display import display, HTML

import os
import argparse
import logging
import warnings
warnings.filterwarnings('ignore')


cur_dir = os.path.dirname(os.path.realpath(__file__))

CSS = """
.output {
    flex-direction: row;
}
"""

HTML('<style>{}</style>'.format(CSS))


class Strategy:
    def __init__(self, stock_data: pd.DataFrame,
                 call_return_data: pd.DataFrame,
                 actions: pd.DataFrame) -> None:
        self.stock_data = stock_data
        self.call_actions = pd.merge(call_return_data, actions, on='call_uid')
        self.init_value = 10_000
        total_actions = len(self.call_actions[self.call_actions.action != 0])
        # days between min_date and max_date
        call_return_data['start_price_date'] = pd.to_datetime(
            call_return_data.start_price_date)
        call_return_data['end_price_date'] = pd.to_datetime(
            call_return_data.end_price_date)
        min_date = call_return_data.start_price_date.min()
        max_date = call_return_data.end_price_date.max()
        total_days = max_date - min_date + pd.Timedelta(days=1)
        # if trade_ratio is None:
        #     self.trade_ratio = 1/(total_actions / total_days.days *
        #                           call_return_data.holding_period.iloc[0])
        # else:
        #     self.trade_ratio = trade_ratio
        self.spy_data = self.stock_data.loc['SPY']
        self.spy_data = self.spy_data.loc[(self.spy_data.index.get_level_values('date') >= min_date) &
                                          (self.spy_data.index.get_level_values('date') < max_date)]
        self.current_holding = dict(
            SPY=self.init_value / self.spy_data.close.iloc[0])
        self.portfolio = pd.DataFrame(
            columns=['date', 'value', 'propotion', 'holding'])

    def portfolio_value(self, date):
        value = 0
        for ticker, holding in self.current_holding.items():
            value += holding * \
                self.stock_data.loc[ticker].loc[date].close
        return value

    def portfolio_propotion(self, date):
        propotion = []
        nav = self.portfolio_value(date)
        for ticker, holding in self.current_holding.items():
            propotion.append(holding *
                             self.stock_data.loc[ticker].loc[date].close / nav)
        return propotion

    def run(self):
        logger = logging.getLogger('run')
        logger.setLevel(logging.INFO)
        for d in self.spy_data.index.to_list():
            # trade
            d_call_actions = self.call_actions.loc[(self.call_actions.start_price_date == d.strftime('%Y-%m-%d'))
                                                   & (self.call_actions.action != 0)]
            if len(d_call_actions) > 0:
                nav = self.portfolio_value(d)
                for _, action_r in d_call_actions.iterrows():
                    if 'open' in action_r.start_price_type:
                        stock_trade_price = self.stock_data.loc[action_r.company_ticker].loc[d].open
                        spy_trade_price = self.spy_data.loc[d].open
                    elif 'close' in action_r.start_price_type:
                        stock_trade_price = self.stock_data.loc[action_r.company_ticker].loc[d].close
                        spy_trade_price = self.spy_data.loc[d].close
                    # trade_values = self.trade_ratio * nav
                    trade_values = 500
                    stock_shares = trade_values / stock_trade_price
                    spy_shares = trade_values / spy_trade_price

                    if action_r.action == 1:
                        # sell spy to buy stock
                        self.current_holding['SPY'] -= spy_shares
                        self.current_holding[action_r.company_ticker] = stock_shares
                    elif action_r.action == -1:
                        # sell stock to buy spy
                        self.current_holding[action_r.company_ticker] = - \
                            stock_shares
                        self.current_holding['SPY'] += spy_shares
                    logger.debug(
                        f"{d} Open Trade: {'Buy' if action_r.action == 1 else 'Sell'} {action_r.company_ticker} {stock_shares} Shares")

            # close trade
            d_call_actions = self.call_actions.loc[(self.call_actions.end_price_date == d.strftime('%Y-%m-%d'))
                                                   & (self.call_actions.action != 0)]
            if len(d_call_actions) > 0:
                for _, action_r in d_call_actions.iterrows():
                    assert action_r.company_ticker in self.current_holding, f"{action_r.company_ticker} not in current holding"
                    stock_trade_price = self.stock_data.loc[action_r.company_ticker].loc[d].close
                    spy_trade_price = self.spy_data.loc[d].close
                    # if stock_shares < 0, means we have to buy stock to close the position through selling spy
                    # if stock_shares > 0, means we have to sell stock to close the position through buying spy
                    stock_shares = self.current_holding[action_r.company_ticker]
                    spy_shares = stock_shares * stock_trade_price / spy_trade_price
                    self.current_holding.pop(action_r.company_ticker)
                    self.current_holding['SPY'] += spy_shares
                    logger.debug(
                        f"{d} Close Trade: {'Long position' if action_r.action == 1 else 'Short position'} of {action_r.company_ticker} ({stock_shares} Shares)")

            # update portfolio
            self.portfolio = pd.concat([self.portfolio, pd.DataFrame([
                {'date': d, 'value': self.portfolio_value(d),
                 'propotion': self.portfolio_propotion(d),
                 'holding': self.current_holding}])], ignore_index=True)
            logger.debug(
                f"{d} Portfolio Holdings: {self.portfolio_propotion(d)} {self.current_holding}")
            logger.info(
                f"{d} Portfolio: {self.portfolio_value(d)}")

    def save_portfolio(self, path):
        self.portfolio.to_parquet(path)


def plot(portfolio, model_name='', save_fig=False, save_path='./strategy_test_plot.html'):
    # plot portfolio value vs SPY value after calling run function
    fig = px.line(portfolio, x='date', y='value', title=model_name)
    if save_fig:
        fig.write_html(save_path)
    else:
        fig.show(renderer='png')


def trade_analysis(actions, holding_period=5):
    """Analyze trade hit ratio, profit, loss, etc.
    """
    call_return_data = load_stock_returns_on_calls('test')[
        ['call_uid', 'excess_return', 'holding_period']]
    call_return_data = call_return_data[call_return_data.holding_period == holding_period]
    actions = pd.merge(actions, call_return_data, on='call_uid')
    actions['win'] = (
        (actions['action'] * actions['excess_return']) > 0).astype(int)
    actions['loss'] = (
        (actions['action'] * actions['excess_return']) < 0).astype(int)
    return pd.DataFrame(
        {
            'total': len(actions),
            'trade': (actions['action'] != 0).sum(),
            'trade_ratio': (actions['action'] != 0).sum() / len(actions),
            'buy_ratio': actions[actions.action == 1].shape[0] / len(actions),
            'sell_ratio': actions[actions.action == -1].shape[0] / len(actions),
            'win': actions['win'].sum(),
            'loss': actions['loss'].sum(),
            'hit_ratio': actions['win'].sum() / (actions['win'].sum() + actions['loss'].sum()) if (actions['action'] != 0).sum() != 0 else 0,
        }, index=['Trade Performance']).T


def calc_performance(portfolio, save_metrics=False, save_path='./strategy_test_performance.csv'):
    tail_risk_confidence_level = 5
    portfolio = portfolio[['date', 'value']].set_index('date').copy()
    returns = portfolio['value'].pct_change().dropna()
    annualized_factor = 252
    num_periods = len(returns)
    # Assuming 252 trading days in a year
    num_years = num_periods / annualized_factor

    # Simple Return
    simple_return = returns.mean() * annualized_factor

    # CAGR (Compound Annual Growth Rate)
    cum_returns = np.cumprod(1 + returns)
    cagr = (cum_returns.iloc[-1] /
            cum_returns.iloc[0]) ** (1 / num_years) - 1

    # Max Drawdown
    drawdown = (cum_returns/(cum_returns.cummax()) - 1)
    max_drawdown = drawdown.min(axis=0)

    # Volatility
    volatility = np.std(returns) * np.sqrt(annualized_factor)

    # SHARP RATIO
    # Assuming 0.02% risk free rate
    sharp_ratio = (simple_return - 0.02) / volatility

    # VaR (Value at Risk at X% confidence level)
    var = np.percentile(returns, tail_risk_confidence_level, axis=0)

    # ETL (Expected Tail Loss at X% confidence level)
    etl = np.mean(returns[returns <= var], axis=0)

    # Create a DataFrame to store the metrics
    metrics = pd.DataFrame({
        'Simple Return(Annualized)': simple_return,
        'CAGR': cagr,
        'Volatility(Annualized)': volatility,
        'Sharp Ratio': sharp_ratio,
        'Max Drawdown': max_drawdown,
        'VaR' + str(100 - tail_risk_confidence_level) + "(daily)": var,
        'ETL' + str(100 - tail_risk_confidence_level) + "(daily)": etl
    }, index=['Portfolio Performance']).T

    if save_metrics:
        metrics.to_csv(save_path, index=False)

    return metrics


def run_strategy(
        action_file=f'{cur_dir}/benchmark_action.csv',
        holding_period=5,
        log_file='',
        save_portfolio_path='./portfolio.parquet',):
    """
    Run strategy using the provided action file, holding period, log file, and save portfolio path.

    Parameters:
        action_file (str): Path to the action file containing the buy / no action / sell actions, (default: './benchmark_action.csv').
        holding_period (int): Holding period for the strategy (1-day, 5-days, or 10-days) (default: 5).
        log_file (str): Path to the log file (default: '').
        save_portfolio_path (str): Path to save the portfolio file containing the portfolio values (default: './portfolio.parquet').

    Returns:
        None
    """
    # set log_file and terminal output
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()] +
        [] if log_file == '' else [logging.FileHandler(log_file)],
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    call_returns = load_stock_returns_on_calls('test')
    call_returns = call_returns[call_returns.holding_period == holding_period]
    stock_data = load_stock_history()
    actions = pd.read_csv(action_file)
    strategy = Strategy(stock_data, call_returns, actions)
    strategy.run()
    strategy.save_portfolio(save_portfolio_path)
    report_strategy_analysis(action_file, save_portfolio_path,
                             holding_period)
    return


def report_strategy_analysis(actions,
                             portfolio,
                             holding_period,
                             model_name='Strategy Portfolio Values'):
    """
    Generate a report of the strategy analysis for a given set of actions and portfolio.
    The report contains
    1. Portfolio performance metrics
    2. Trade performance metrics
    3. Portfolio value plot    

    Parameters:
        actions (str): Path to the CSV file containing the actions.
        portfolio (str): Path to the Parquet file containing the portfolio values generated by run_strategy function.
        holding_period (int): The holding period of the strategy (1, 5, or 10 days).
        model_name (str, optional): The name of the model used for plotting title. Defaults to 'Strategy Portfolio Values'.

    Returns:
        None
    """
    actions = pd.read_csv(actions)
    portfolio = pd.read_parquet(portfolio)
    plot(portfolio, model_name=model_name)
    # display dataframe in html
    display(HTML(calc_performance(portfolio).to_html()))
    display(HTML(trade_analysis(actions, holding_period).to_html()))


def demo_benchmark(strategy='spy', holding_period=5):
    """Run benchmark strategy.

    Parameters
    ----------
    strategy : str
        Strategy name. 'spy' or 'random'.
    holding_period : int
        Holding period (1, 5, 10 days) only used when strategy is 'random'. Default is 5.

    Returns
    -------
    None
    """
    report_strategy_analysis(
        f'{cur_dir}/{strategy}_action.csv',
        f'{cur_dir}/{strategy}_strategy_portfolio_{holding_period}d.parquet' if strategy != 'spy' else f'{cur_dir}/{strategy}_strategy_portfolio.parquet',
        holding_period=holding_period,
        model_name='Benchmark Strategy ' + strategy.upper())


def main():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--actions', type=str, help="Path of action file", default=f'{cur_dir}/benchmark_action.csv')
    parser.add_argument('--holding_period', type=int,
                        help="Holding period", default=5)
    parser.add_argument('--log_file', type=str,
                        help="to save the logs", default="")
    parser.add_argument('--save_path', type=str,
                        help="to save the portfolio", default="./portfolio.parquet")

    args = parser.parse_args()
    run_strategy(action_file=args.actions,
                 holding_period=args.holding_period,
                 log_file=args.log_file,
                 save_portfolio_path=args.save_path)


if __name__ == '__main__':
    main()
