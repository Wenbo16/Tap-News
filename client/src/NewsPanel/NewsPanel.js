import './NewsPanel.css';
import React from 'react';
import NewsCard from '../NewsCard/NewsCard';
import RecommendNewsCard from '../RecommendNewsCard/RecommendNewsCard';
import Auth from '../Auth/Auth';
import _ from 'lodash';

class NewsPanel extends React.Component {
    constructor() {
        super();
        this.state = { news:null, recommendNews:null, pageNum:1, loadedAll:false};
        this.getSimilarNews = this.getSimilarNews.bind(this);
    }   


    // after constructor excuted
    componentDidMount() {
        this.loadMoreNews();
        // wrap loadMoreNews
        this.loadMoreNews = _.debounce(this.loadMoreNews, 500);
        window.addEventListener('scroll', this.handleScroll.bind(this));
    }

    handleScroll() {
        let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
            console.log('Loading more news...');
            this.loadMoreNews();
        }
    }

    loadMoreNews() {
        if(this.state.loadedAll === true){
            return;
        }

        let url = 'http://localhost:3000/news/userId/' + encodeURIComponent(Auth.getEmail())
                  + '/pageNum/' + encodeURIComponent(this.state.pageNum);
        console.log('Page: ', this.state.pageNum)          
        // escape special charactor
        let request = new Request(url, {
            method: 'GET',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false
        });

        fetch(request)
            .then((res) => res.json())
            .then((news) => {
                if(!news || news.length === 0){
                    this.setState({loadedAll: true});
                }

                this.setState({
                    news: this.state.news ? this.state.news.concat(news) : news,
                    pageNum: this.state.pageNum + 1
                });
            });
    }

    getSimilarNews(news){
        this.setState({recommendNews: news});
    }


    renderNews() {
        const news_list = this.state.news.map(function(news) {
            return (
                <a className="list-group-item"  href='#'> 
                    <NewsCard news={news} getSimilarNews={this.getSimilarNews}/>
                </a>
            );
        }, this);

        return (
                <div className='list-group'>
                    {news_list}
                </div>
        );
    }
     
    renderRecommendNews() {
        if(this.state.recommendNews !== null){
            console.log(this.state.recommendNews);
            const recommend_news_list = this.state.recommendNews.map(function(news) {
                return (
                    <a className="list-group-item"  href='#'> 
                        <RecommendNewsCard news={news}/>
                    </a>
                );
            }, this);

            return (
                <div className='list-group'>
                    {recommend_news_list}
                </div>
            );
        }
        return (
            <p></p>
        );
    }


    render() {
        if (this.state.news) {
            return (
                <div className="row">
                    <div className="col s9">
                        {this.renderNews()}
                    </div>
                    <div className='col s3'>
                        <h5> You may like:</h5>
                        {this.renderRecommendNews()}
                    </div>
                </div>
            );
        } else {
            return (
                <div>
                    Loading...
                </div>
            )
        }
    }
}

export default NewsPanel;
