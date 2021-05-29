import './App.css';
import React, { useEffect, useCallback } from 'react';
<<<<<<< HEAD
import { Route, Switch, useLocation } from 'react-router-dom';
=======
import { Route, Switch, useLocation, useHistory } from 'react-router-dom';
>>>>>>> feature_UI/UX
import Home from './pages/Home';
import Main from './pages/Main';
import AuthRoute from './AuthRoute';
import { SERVER_URL } from './config';
import axios from 'axios';
<<<<<<< HEAD
import MyPage from './pages/MyPage';
import { useLocalStorage } from './customHooks/useLocalStorage';
import UserInfo from './pages/UserInfo';
import WithDraw from './pages/Withdraw';
function App() {
  const location = useLocation();
=======
import { useLocalStorage } from './customHooks/useLocalStorage';
import UserInfo from './pages/UserInfo';
import WithDraw from './pages/Withdraw';
import Game from './pages/Game';
import MyPageIntro from './pages/MyPageIntro';
import ComponentsChart from './pages/ComponentsChart';

function App() {
  const location = useLocation();
  const history = useHistory();
>>>>>>> feature_UI/UX

  const [token, setToken] = useLocalStorage('access_token', null);

  const checkTokenState = useCallback(async () => {
    const AuthStr = `Bearer ${localStorage.getItem('access_token')}`;
    try {
      const res = await axios.get(SERVER_URL + '/protected', {
        headers: {
          Authorization: AuthStr,
        },
      });
    } catch (error) {
      alert(error);
<<<<<<< HEAD
      setToken(null);
      // // //로그아웃 된다는 모달? alert 띄워주기?
      localStorage.removeItem('access_token');
    }
  }, [setToken]);
=======
      // setToken(null);
      //위 코드 없어도 에러 안 날것 같아서 일단 주석. 에러 나면 주석해제하기
      history.push('/');
      // // //로그아웃 된다는 모달? alert 띄워주기?
      localStorage.removeItem('access_token');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
>>>>>>> feature_UI/UX

  useEffect(() => {
    if (localStorage.getItem('access_token')) {
      checkTokenState();
    }
<<<<<<< HEAD
  }, [location, token, checkTokenState]);
=======
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location]);
>>>>>>> feature_UI/UX
  //페이지가 변할때마다 로그인 여부 확인

  return (
    <div className="App">
      <Switch>
        <Route path="/" exact render={(props) => <Home {...props} />} />
        {/* login 되어있다면 main("/main"), 되어있지 않다면 home("/")으로 처리 */}
        <AuthRoute path="/main" render={(props) => <Main {...props} />} />
        <AuthRoute
          path="/mypage"
          exact
<<<<<<< HEAD
          render={(props) => <MyPage {...props} />}
        />
=======
          render={(props) => <MyPageIntro {...props} />}
        />
        {/* <AuthRoute
          path="/mypage/confirm"
          exact
          render={(props) => <MyPageIntro {...props} />}
        /> */}
>>>>>>> feature_UI/UX
        <AuthRoute
          path="/mypage/userinfo"
          render={(props) => <UserInfo {...props} />}
        />
        <AuthRoute
<<<<<<< HEAD
          path="/mypage/signout"
          render={(props) => <WithDraw {...props} />}
        />
        {/* login 필요한 경로들은 AuthRoute로 배정하기 */}
=======
          path="/mypage/withdraw"
          render={(props) => <WithDraw {...props} />}
        />
        <AuthRoute path="/game" render={(props) => <Game {...props} />} />
        {/* login 필요한 경로들은 AuthRoute로 배정하기 */}
        <Route path="/components" component={ComponentsChart} />
>>>>>>> feature_UI/UX
      </Switch>
    </div>
  );
}

export default App;
