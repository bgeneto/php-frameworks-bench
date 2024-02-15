<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpKernel\Kernel;


class HelloController extends AbstractController
{
    #[Route('/')]
	public function index(): Response
	{
        $version = Kernel::VERSION;
		return $this->render('welcome.html.twig', ['version' => $version]);
	}

    #[Route('/benchmarking/hello')]
    public function hello(): Response
    {
        $data = ['output'=>'Hello, World!!!'];
        return $this->render('benchmarking/hello.html.twig', $data);
    }
}
