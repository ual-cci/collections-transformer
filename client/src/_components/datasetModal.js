'use client'

import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

const DatasetModal = ({
  children,
  props,
  onPressHandler,
  id,
  title="",
  iconName="",
  warningText="",
  buttonActionText="",
  canCancel=true,
  isButton=true,
  modalSize="lg"
}) => {




  
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const handlePress = () => {
    onPressHandler(id)
    handleClose()
  }

  // Custom button styling if provided
  const buttonStyle = props?.buttonStyle || {};
  const buttonHoverStyle = props?.buttonHoverStyle || {};

  return (
    <>
      {isButton ? (
        <Button 
          variant={props?.buttonStyle ? undefined : "outline-dark"}
          className="material-symbols-outlined" 
          onClick={handleShow}
          style={buttonStyle}
          onMouseEnter={props?.buttonStyle ? (e) => Object.assign(e.target.style, buttonHoverStyle) : undefined}
          onMouseLeave={props?.buttonStyle ? (e) => Object.assign(e.target.style, buttonStyle) : undefined}
        >
          {iconName}
        </Button>
      ) : (
        <span className="material-symbols-outlined" onClick={handleShow}>{iconName}</span>
      ) }

      <Modal 
        show={show} 
        onHide={handleClose}
        {...props}
        size={modalSize}
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>{title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>{children}</div><br/>
          {warningText.length>0 ? (<div className="warning-box">{warningText}</div>) : <></>}
        </Modal.Body>
      </Modal>
    </>
  );
}

export default DatasetModal;
