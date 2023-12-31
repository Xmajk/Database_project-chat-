USE [master]
GO
/****** Object:  Database [python]    Script Date: 08.03.2023 23:06:51 ******/
CREATE DATABASE [python]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'python', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\python.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'python_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\python_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [python] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [python].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [python] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [python] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [python] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [python] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [python] SET ARITHABORT OFF 
GO
ALTER DATABASE [python] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [python] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [python] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [python] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [python] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [python] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [python] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [python] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [python] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [python] SET  DISABLE_BROKER 
GO
ALTER DATABASE [python] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [python] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [python] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [python] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [python] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [python] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [python] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [python] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [python] SET  MULTI_USER 
GO
ALTER DATABASE [python] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [python] SET DB_CHAINING OFF 
GO
ALTER DATABASE [python] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [python] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [python] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [python] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [python] SET QUERY_STORE = OFF
GO
USE [python]
GO
/****** Object:  Table [dbo].[MHMssgs]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MHMssgs](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[predmet] [nvarchar](250) NOT NULL,
	[od] [int] NULL,
	[pro] [int] NULL,
	[txt] [nvarchar](max) NOT NULL,
	[odeslano] [datetime] NOT NULL,
	[tmp_od] [nvarchar](50) NULL,
	[tmp_pro] [nvarchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[MHUsers]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MHUsers](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[username] [nvarchar](50) NULL,
	[psswd] [nvarchar](400) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[MHMssgs]  WITH CHECK ADD FOREIGN KEY([od])
REFERENCES [dbo].[MHUsers] ([id])
GO
ALTER TABLE [dbo].[MHMssgs]  WITH CHECK ADD FOREIGN KEY([od])
REFERENCES [dbo].[MHUsers] ([id])
GO
/****** Object:  StoredProcedure [dbo].[mp_delete_od]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_delete_od] @id as int AS
BEGIN
    IF EXISTS (SELECT * FROM MHMssgs WHERE id = @id AND pro IS NOT NULL)
    BEGIN
        UPDATE MHMssgs SET od = NULL WHERE id = @id
    END
    ELSE
    BEGIN
        DELETE FROM MHMssgs WHERE id = @id
    END
END;
GO
/****** Object:  StoredProcedure [dbo].[mp_delete_pro]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_delete_pro] @id as int AS
BEGIN
    IF EXISTS (SELECT * FROM MHMssgs WHERE id = @id AND od IS NOT NULL)
    BEGIN
        UPDATE MHMssgs SET pro = NULL WHERE id = @id
    END
    ELSE
    BEGIN
        DELETE FROM MHMssgs WHERE id = @id
    END
END;
GO
/****** Object:  StoredProcedure [dbo].[mp_obdzel_id]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_obdzel_id] @username as nvarchar(50) AS
SELECT m.id FROM MHUsers u inner join MHMssgs m on u.id=m.pro
where u.username=@username;
GO
/****** Object:  StoredProcedure [dbo].[mp_select_all_users]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_select_all_users] AS
select username from MHUsers;
GO
/****** Object:  StoredProcedure [dbo].[mp_select_dorucene_basic]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_select_dorucene_basic] @username as nvarchar(50) AS
SELECT m.id,m.predmet,m.odeslano,m.tmp_od from 
(MHUsers u right join MHMssgs m on u.id=m.pro) left join MHUsers u2
on u2.id=m.od
where u.username=@username and m.tmp_od is not null order by m.odeslano ASC,m.id ASC;
GO
/****** Object:  StoredProcedure [dbo].[mp_select_dorucene_basic_limit]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_select_dorucene_basic_limit] @username as nvarchar(50), @limit as int AS
SELECT * FROM(SELECT TOP(@limit) m.id,m.predmet,m.odeslano,m.tmp_od from 
(MHUsers u right join MHMssgs m on u.id=m.pro) left join MHUsers u2
on u2.id=m.od
where u.username=@username and m.tmp_od is not null order by m.odeslano DESC,m.id DESC) s order by s.odeslano ASC,s.id ASC;
GO
/****** Object:  StoredProcedure [dbo].[mp_select_id_by_username]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_select_id_by_username] @username as nvarchar(50) AS
select id from MHUsers where username=@username;
GO
/****** Object:  StoredProcedure [dbo].[mp_select_mssg_by_id]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_select_mssg_by_id] @id as int AS
SELECT m.tmp_pro,m.tmp_od,m.id,m.predmet,m.txt,m.odeslano from 
(MHUsers u right join MHMssgs m on u.id=m.pro) left join MHUsers u2
on u2.id=m.od
WHERE m.id=@id and m.tmp_pro is not null and m.tmp_od is not null
GO
/****** Object:  StoredProcedure [dbo].[mp_select_odeslane_basic]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_select_odeslane_basic] @username as nvarchar(50) AS
SELECT m.id,m.predmet,m.odeslano,m.tmp_pro from 
(MHUsers u right join MHMssgs m on u.id=m.pro) left join MHUsers u2
on u2.id=m.od
where u2.username=@username and m.tmp_pro is not null order by m.odeslano ASC,m.id ASC;--desc
GO
/****** Object:  StoredProcedure [dbo].[mp_select_odeslane_basic_limit]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_select_odeslane_basic_limit] @username as nvarchar(50), @limit as int AS
SELECT * FROM(SELECT TOP(@limit) m.id,m.predmet,m.odeslano,m.tmp_pro from 
(MHUsers u right join MHMssgs m on u.id=m.pro) left join MHUsers u2
on u2.id=m.od
where u2.username=@username and m.tmp_pro is not null order by m.odeslano DESC,m.id DESC) s order by s.odeslano ASC,s.id ASC;--DeSC
GO
/****** Object:  StoredProcedure [dbo].[mp_sended_id]    Script Date: 08.03.2023 23:06:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[mp_sended_id] @username as nvarchar(50) AS
SELECT m.id FROM MHUsers u inner join MHMssgs m on u.id=m.od
where u.username=@username;
GO
USE [master]
GO
ALTER DATABASE [python] SET  READ_WRITE 
GO
