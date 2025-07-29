'use client'

import { 
    Sidebar,
    Menu,
    SubMenu,
    MenuItem
  } from "react-pro-sidebar";
import Link from 'next/link'
import Image from 'next/image'
import { useUser } from "@auth0/nextjs-auth0/client";
import logo from '../../public/ual-logo.png'
import { useState } from "react";


const SideBar = () => {

    const { user, error, isLoading } = useUser();

    const [collapsed, setCollapsed] = useState(false)

    return (
        <div className="sidebar-container flex">
            <Sidebar collapsed={collapsed}>
                <div className="sidebar-inner">
                    
                    <div className="sidebar-top">
                        <Menu>
                            
                            <MenuItem icon={<span className='material-symbols-outlined'>home</span>} component={<Link href="/" />}> Home </MenuItem>

                            <MenuItem icon={<span className='material-symbols-outlined'>account_circle</span>} component={<Link href="/user" />}> Your Profile </MenuItem>

                            <MenuItem icon={<span className='material-symbols-outlined'>hub</span>} component={<Link href="/ecosystem" />}> Your Workspace </MenuItem>
                            
                            <MenuItem icon={<span className='material-symbols-outlined'>psychology</span>} component={<Link href="/newmodel" />}> New Model </MenuItem>
                            
                            
                            <MenuItem icon={<span className='material-symbols-outlined'>upload</span>} component={<Link href="/uploaddataset" />}> New Dataset </MenuItem>

                            <MenuItem icon={<span className='material-symbols-outlined'>pattern</span>} component={<Link href="/findpatterns" />}> Analytical Task </MenuItem>


                            <MenuItem icon={<span className='material-symbols-outlined'>help</span>} component={<Link href="/about" />}> FAQ </MenuItem>
                            
                            <hr></hr>
                        </Menu>
                    </div>
                    
                    <div className="sidebar-bottom">   
                        <Menu>
                            <hr></hr>
                            {user ? (
                                <MenuItem icon={<span className='material-symbols-outlined'>logout</span>} component={<a href="/api/auth/logout"/>}> Logout ({user.name === user.email ? user.nickname : user.name})</MenuItem> 
                            )
                            : (
                                <MenuItem icon={<span className='material-symbols-outlined'>login</span>} component={<a href="/api/auth/login"/>}> Login </MenuItem> 
                            )}
                        </Menu>
                        <div style={{ display: "flex", justifyContent: "center" }}>
                            <Image 
                                src={logo}
                                width={collapsed ? 50 : 150}
                                alt="University Arts London Logo"
                            />
                        </div>
                    </div>
                </div>
            </Sidebar>
        </div>
    )
}

export default SideBar

