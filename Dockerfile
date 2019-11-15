FROM alpacamarkets/pylivetrader

RUN pip3 uninstall -y iexfinance
RUN pip3 uninstall -y iexfinance
RUN pip install iexfinance

ARG APCA_API_SECRET_KEY
ARG APCA_API_KEY_ID
ARG APCA_API_BASE_URL
ARG IEX_API_VERSION
ARG IEX_TOKEN

ENV APCA_API_SECRET_KEY=$APCA_API_SECRET_KEY
ENV APCA_API_KEY_ID=$APCA_API_KEY_ID
ENV APCA_API_BASE_URL=$APCA_API_BASE_URL
ENV IEX_API_VERSION=$IEX_API_VERSION
ENV IEX_TOKEN=$IEX_TOKEN

RUN mkdir /app

COPY . /app

WORKDIR /app

CMD pylivetrader run -f algo.py
