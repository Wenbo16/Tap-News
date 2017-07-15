import './RecommendNewsCard.css';

import React from 'react';
import Auth from '../Auth/Auth';

class NewsCard extends React.Component {
    constructor() {
        super();
        this.redirectToUrl = this.redirectToUrl.bind(this);
    }

    redirectToUrl(event) {
        event.preventDefault();
        this.sendClickLog();
        window.open(this.props.news.url, '_blank');
    }


    render() {
        return (
            <div className="recommend-news-container" onClick={this.redirectToUrl}>
                <div className="recommend-news-intro-col">
                    <p>{this.props.news.title}</p>
                </div> 
                <div className="side-img">
                    <img src={this.props.news.urlToImage} alt='news' />
                </div>
            </div>
        );
    }
}

export default NewsCard;
