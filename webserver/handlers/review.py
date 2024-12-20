#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import datetime
from gettext import gettext as _

import tornado.escape
from webserver.handlers.base import BaseHandler, auth, js
from webserver.models import Review, ReviewBook

from sqlalchemy import func


class ReviewSummary(BaseHandler):
    def should_be_invited(self):
        pass

    @js
    def get(self):
        cfi_base = self.get_argument("cfi_base", "").strip()
        title = self.get_argument("title", "").strip().lower()
        if not cfi_base or not title:
            return {"err": "params.invalid", "msg": _(u"参数错误")}
        q = self.session.query(Review.segment_id, func.count().label('cnt'))
        q = q.filter(Review.title == title).group_by(Review.segment_id)

        data = []
        for row in q.all():
            segment_id, cnt = row
            data.append({"segmentId": segment_id, "reviewNum": cnt})
        return {"err": "ok", "data": {"list": data}}
 

class ReviewList(BaseHandler):
    def should_be_invited(self):
        pass

    @js
    def get(self):
        cfi_base = self.get_argument("cfi_base", "").strip()
        title = self.get_argument("title", "").strip().lower()
        segment_id = self.get_argument("segment_id", "").strip()
        if not cfi_base or not title or not segment_id:
            return {"err": "params.invalid", "msg": _(u"参数错误")}
        
        q = self.session.query(Review).fliter(
            Review.title == title,
            Review.cfi_base == cfi_base,
            Review.segment_id == segment_id)

        data = []
        for row in q.all():
            d = row.to_full_dict()
            d['isSelf'] = row.user.id == self.current_user.id
            d['ipAddress'] = self.request.remote_ip
            data.append(row.to_full_dict())

        return {"err": "ok", "data": {"list": data}}
    
        demo =       {
        "reviewId": "1063367226805911552",
        "cbid": "25583693309808304",
        "ccid": "69203747871449297",
        "guid": "854065516235",
        "userId": "409829755",
        "nickName": "约克君",
        "avatar": "https://qidian.gtimg.com/qd/images/ico/default_user.0.2.png",
        "segmentId": 5,
        "content": "好地方，不会饿[fn=18]",
        "status": 1,
        "createTime": "10-15 08:37:59",
        "createTimestamp": 1728952679,
        "updateTime": "2024-11-16 13:36:10",
        "quoteReviewId": "0",
        "quoteContent": "",
        "quoteGuid": "0",
        "quoteUserId": "0",
        "quoteNickName": "",
        "type": 2,
        "likeCount": 9,
        "dislikeCount": 0,
        "userLike": false,
        "userDislike": false,
        "isSelf": false,
        "essenceStatus": false,
        "riseStatus": false,
        "level": 948,
        "imagePre": "",
        "imageDetail": "",
        "rootReviewId": "1063367226805911552",
        "rootReviewReplyCount": 0,
        "ipAddress": "上海"
      }


class ReviewAdd(BaseHandler):
    @js
    @auth
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        if not data:
            return {"err": "params.invalid", "msg": _(u"参数错误")}
        
        review = Review(**data)
        review.user = self.current_user.id
        review.save()

        review.quote.update_time = datetime.datetime.now()
        review.quote.save()

        review.root.update_time = datetime.datetime.now()
        review.root.save()
        return {"err": "ok"}


class ReviewMe(BaseHandler):
    @js
    @auth
    def get(self):
        is_count = self.get_argument("count", "").strip() != ""
        last_read = self.current_user.extra.get("last_read", "")
        q = self.session.query(Review).filter(Review.user == self.current_user.id)
        if last_read:
            q = q.filter(Review.update_time > last_read)
        else:
            q = q.filter(Review.update_time > Review.create_time)

        if is_count:
            return {"err": "ok", "data": {"count": q.count()}}

        data = []
        for row in q.all():
            d = row.to_full_dict()
            d['isSelf'] = row.user.id == self.current_user.id
            d['ipAddress'] = self.request.remote_ip
            data.append(row.to_full_dict())

        return {"err": "ok", "data": {"list": data}}


class ReviewGetBook(BaseHandler):
    @js
    def get(self):
        title = self.get_argument("title", "").strip().lower()
        calibre_id = int(self.get_argument("calibre_id", 0).strip())

        if not title or not calibre_id:
            return {"err": "params.invalid", "msg": _(u"参数错误")}

        row = self.session.query(ReviewBook).filter(ReviewBook.calibre_id == calibre_id).first()
        if row:
            return {"err": "ok", "data": row.to_dict()}

        row = self.session.query(ReviewBook).filter(ReviewBook.title == title).first()
        if row:
            return {"err": "ok", "data": row.to_dict()}

        row = self.session.query(ReviewBook).filter(ReviewBook.alias.like(f'%{title}%')).first()
        if row:
            return {"err": "ok", "data": row.to_dict()}

        row = ReviewBook()
        row.title = title
        row.alias = title
        row.calibre_id = calibre_id
        row.save()
        return {"err": "ok", "data": row.to_dict()}


def routes():
    return [
        (r"/api/review/book", ReviewGetBook),
        (r"/api/review/summary", ReviewSummary),
        (r"/api/review/list", ReviewList),
        (r"/api/review/add", ReviewAdd),
        (r"/api/review/me", ReviewMe),
    ]
