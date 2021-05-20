import CustomSignIn from '../components/CustomSignIn';
import UserInfoForm from '../components/UserInfoForm';
import 'react-datepicker/dist/react-datepicker.css';
import { SERVER_URL } from '../config';
import axios from 'axios';
import { useRecoilState } from 'recoil';
import {
  loggedinState,
  signInModalOpenState,
  signUpModalOpenState,
} from '../states/state';
import React from 'react';
import { Redirect } from 'react-router';

const Home = ({ location }) => {
  const [isLoggedIn, setIsLoggedIn] = useRecoilState(loggedinState);
  const [openSignIn, setOpenSignIn] = useRecoilState(signInModalOpenState);
  const [openSignUp, setOpenSignUp] = useRecoilState(signUpModalOpenState);

  const { from } = location.state || { from: { pathname: '/main' } };
  if (isLoggedIn) {
    return <Redirect to={from} />;
    //로그인 된 상태라면 직전에 있었던 페이지 혹은 main으로 redirect된다.
    //redirect 되는 과정에서 아래에서 리턴되는 화면이 보여지는데 이걸 막는 방법이 있을까?
  }
  const handleSignUp = async (data) => {
    try {
      const res = await axios.post(SERVER_URL + '/sign-up', data);
      console.log(res);
      //로그인도 시켜주기
    } catch (error) {
      alert(error);
      //회원가입이 된 유저라면 로그인 창 띄워주기
    }
  }; //회원가입 요청

  const handleCustomSignIn = async (data) => {
    try {
      const res = await axios.post(SERVER_URL + '/sign-in', data);
      localStorage.setItem('access_token', res.data.access_token);
      localStorage.setItem('refresh_token', res.data.refresh_token);
      setIsLoggedIn(true);
      setOpenSignIn(false);
      //state에 사용자 닉네임도 저장해주기
      //로그인 후 main화면으로 이동
    } catch (error) {
      alert(error);
    }
    // const res = await axios.post(SERVER_URL + '/sign-in', data);
    // console.log(res);
    // if ((res.data.status = 200)) {
    //   localStorage.setItem('access_token', res.data.access_token);
    //   localStorage.setItem('refresh_token', res.data.refresh_token);
    //   setIsLoggedIn(true);
    //   setOpenSignIn(false);
    // }
  }; //로그인 요청

  return (
    <div className="home-container">
      {!openSignIn && !openSignUp ? (
        <div className="home-button-group">
          <input
            type="button"
            value="Sign In"
            onClick={() => {
              setOpenSignIn(!openSignIn);
            }}
          />
          <input
            type="button"
            value="Sign Up"
            onClick={() => {
              setOpenSignUp(!openSignUp);
            }}
          />
        </div>
      ) : null}
      {openSignIn ? (
        <div className="signin-modal">
          <CustomSignIn handleCustomSignIn={handleCustomSignIn} />
          <button
            type="button"
            onClick={() => {
              setOpenSignIn(!openSignIn);
            }}
          >
            &#10006;
          </button>
        </div>
      ) : null}
      {openSignUp ? (
        <div className="signup-modal">
          <UserInfoForm handleUserInfoForm={handleSignUp} />
          <button
            type="button"
            onClick={() => {
              setOpenSignUp(!openSignUp);
            }}
          >
            &#10006;
          </button>
        </div>
      ) : null}
    </div>
  );
};

export default Home;
