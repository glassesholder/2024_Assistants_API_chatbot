"""
파일 관리 모듈
업로드된 파일의 저장, 삭제 등을 담당합니다.
"""
import os
import streamlit as st
from config import UPLOAD_DIRECTORY

def save_uploaded_file(uploaded_file):
    """업로드된 파일을 로컬에 저장"""
    file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def cleanup_files(file_paths):
    """파일 목록을 삭제"""
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except Exception as e:
            st.warning(f"파일 삭제 중 오류 발생: {file_path}")

def prepare_file_handles(uploaded_files):
    """업로드된 파일들을 처리하여 파일 핸들과 경로를 반환"""
    file_paths = []
    file_handles = []
    
    try:
        # 파일 저장
        for uploaded_file in uploaded_files:
            file_path = save_uploaded_file(uploaded_file)
            file_paths.append(file_path)
            file_handle = open(file_path, 'rb')
            file_handles.append(file_handle)
        
        return file_handles, file_paths
    
    except Exception as e:
        # 오류 발생시 이미 열린 파일 핸들들 정리
        for handle in file_handles:
            try:
                handle.close()
            except:
                pass
        cleanup_files(file_paths)
        raise e

def close_file_handles(file_handles):
    """파일 핸들들을 안전하게 닫기"""
    for handle in file_handles:
        try:
            handle.close()
        except:
            pass
